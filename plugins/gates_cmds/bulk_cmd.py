import re
import asyncio
from typing import Dict, List
from pyrogram import filters
from pyromod import Client
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from utilsdf.db import Database
from utilsdf.vars import PREFIXES
from utilsdf.functions import get_cc, get_text_from_pyrogram
from utilsdf.gate_registry import get_all_gateways
from utilsdf.bulk_engine import run_bulk_checker_task
from utilsdf.logger import logger

# Temporary storage for bulk card sessions before gateway selection
bulk_sessions: Dict[int, List[tuple]] = {}


def build_bulk_gate_keyboard(page: int = 1) -> InlineKeyboardMarkup:
    """Builds an interactive Inline Keyboard for Gateway selection in Bulk Check."""
    gateways = get_all_gateways()
    
    # Categorize gateways
    auth_gates = [(cmd, info) for cmd, info in gateways.items() if info["category"] == "Auth"]
    charged_gates = [(cmd, info) for cmd, info in gateways.items() if info["category"] == "Charged"]
    shopify_gates = [(cmd, info) for cmd, info in gateways.items() if info["category"] == "Shopify"]
    
    pages = {1: auth_gates, 2: charged_gates, 3: shopify_gates}
    current_list = pages.get(page, auth_gates)
    
    buttons = []
    # Build 2 buttons per row
    row = []
    for cmd, info in current_list:
        btn_text = f"{info['name']} ({info['price']})"
        row.append(InlineKeyboardButton(btn_text, callback_data=f"blk_gate_{cmd}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    # Navigation row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"blk_page_{page - 1}"))
    if page < 3:
        nav_row.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"blk_page_{page + 1}"))
    if nav_row:
        buttons.append(nav_row)

    buttons.append([InlineKeyboardButton("لغو ❌", callback_data="blk_cancel")])
    return InlineKeyboardMarkup(buttons)


@Client.on_message(filters.command(["blk", "bulk"], PREFIXES))
async def bulk_cmd(client: Client, m: Message):
    user_id = m.from_user.id
    
    # Verify Admin or Authorized User
    with Database() as db:
        if not db.is_seller_or_admin(user_id) and str(user_id) != str(db.ID_OWNER):
            if not db.is_premium(user_id):
                return await m.reply("<b>❌ این دستور فقط برای مدیران و کاربران ویژه فعال است.</b>", quote=True)

    text = get_text_from_pyrogram(m)
    
    # Extract CCs from the command text or reply message
    extracted_cards = []
    if m.reply_to_message:
        reply_text = get_text_from_pyrogram(m.reply_to_message)
        extracted_cards = extract_all_ccs(reply_text)
    else:
        extracted_cards = extract_all_ccs(text)

    # If no cards found in the message, prompt the user for input
    if not extracted_cards:
        prompt_msg = await m.reply(
            "<b>📥 لطفا لیست کارت‌های اعتباری خود را ارسال کنید (هر کارت در یک خط):</b>\n\n"
            "<i>مثال:</i>\n<code>5550600133470666|02|30|094\n5466351319135250|02|31|137</code>",
            quote=True,
        )
        try:
            response_msg: Message = await client.listen(m.chat.id, timeout=60)
            if response_msg and response_msg.text:
                extracted_cards = extract_all_ccs(response_msg.text)
        except Exception:
            return await prompt_msg.edit_text("<b>⏱ زمان ارسال اطلاعات به پایان رسید.</b>")

    if not extracted_cards:
        return await m.reply("<b>❌ هیچ کارت معتبری یافت نشد! لطفا فرمت cc|mm|yy|cvv را رعایت کنید.</b>", quote=True)

    # Store cards in session
    bulk_sessions[user_id] = extracted_cards
    total_count = len(extracted_cards)

    menu_text = f"""<b>📊 بررسی دسته‌جمعی (Bulk Check) »</b>

<b>تعداد کارت‌های شناسایی شده:</b> <code>{total_count}</code>

<code>لطفا درگاه مورد نظر جهت بررسی صف FIFO را انتخاب کنید:</code>"""

    await m.reply_text(
        text=menu_text,
        reply_markup=build_bulk_gate_keyboard(page=1),
        quote=True,
    )


def extract_all_ccs(text: str) -> List[tuple]:
    """Extracts all valid credit cards matching cc|mm|yy|cvv from multiline text."""
    cards = []
    if not text:
        return cards
    pattern = r"(\d{15,16})[\s|/:,-]+(\d{1,2})[\s|/:,-]+(\d{2,4})[\s|/:,-]+(\d{3,4})"
    matches = re.findall(pattern, text)
    for match in matches:
        cc, month, year, cvv = match
        month = month.zfill(2)
        if len(year) == 2:
            year = "20" + year
        cards.append((cc, month, year, cvv))
    return cards


@Client.on_callback_query(filters.regex(r"^blk_page_"))
async def bulk_page_callback(client: Client, callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[-1])
    user_id = callback_query.from_user.id
    cards = bulk_sessions.get(user_id, [])
    total_count = len(cards)

    page_names = {1: "احراز هویت (Auth)", 2: "شارژی (Charged)", 3: "شاپیفای (Shopify)"}
    page_title = page_names.get(page, "درگاه‌ها")

    menu_text = f"""<b>📊 بررسی دسته‌جمعی (Bulk Check) » {page_title}</b>

<b>تعداد کارت‌های شناسایی شده:</b> <code>{total_count}</code>

<code>لطفا درگاه مورد نظر جهت بررسی صف FIFO را انتخاب کنید:</code>"""

    await callback_query.message.edit_text(
        text=menu_text,
        reply_markup=build_bulk_gate_keyboard(page=page),
    )


@Client.on_callback_query(filters.regex(r"^blk_gate_"))
async def bulk_gate_select_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    gate_cmd = callback_query.data.replace("blk_gate_", "")

    cards = bulk_sessions.pop(user_id, None)
    if not cards:
        return await callback_query.answer("❌ جلسه بررسی منقضی شده است. لطفا دوباره /blk را ارسال کنید.", show_alert=True)

    gateways = get_all_gateways()
    gate_info = gateways.get(gate_cmd)
    gate_name = gate_info["name"] if gate_info else gate_cmd

    await callback_query.message.edit_text(
        f"<b>✅ درگاه <code>{gate_name}</code> انتخاب شد. صف FIFO برای {len(cards)} کارت آغاز گردید...</b>"
    )

    # Launch asynchronous FIFO processing task
    asyncio.create_task(run_bulk_checker_task(client, user_id, chat_id, gate_cmd, cards))


@Client.on_callback_query(filters.regex(r"^blk_cancel$"))
async def bulk_cancel_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bulk_sessions.pop(user_id, None)
    await callback_query.message.edit_text("<b>❌ عملیات بررسی دسته‌جمعی لغو شد.</b>")
