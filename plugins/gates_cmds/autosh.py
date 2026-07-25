import traceback, re, asyncio
from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.db import Database
from utilsdf.functions import (
    anti_bots_telegram,
    get_bin_info,
    get_cc,
    antispam,
    get_text_from_pyrogram,
    user_not_premium,
)
from utilsdf.vars import PREFIXES
from gates.autosh import autoshopify


@Client.on_message(filters.command(["autosh", "sh", "shopify"], PREFIXES))
async def autosh_cmd(client: Client, m: Message):
    user_id = m.from_user.id
    
    with Database() as db:
        is_premium = db.is_premium(user_id)
        user_info = db.get_info_user(user_id)
        credits = user_info.get("CREDITS", 0)

        if not is_premium:
            await user_not_premium(m)
            return

        is_free_user = user_info["MEMBERSHIP"].lower() == "free user"
        if is_free_user:
            captcha = await anti_bots_telegram(m, client)
            if not captcha:
                return

    text = get_text_from_pyrogram(m)
    ccs = get_cc(text)
    
    if not ccs:
        return await m.reply(
            "<b>درگاه شاپیفای (Auto Shopify) ♻️</b>\n"
            "فرمت: <code>/autosh cc|month|year|cvc</code> یا <code>/autosh site.com cc|month|year|cvc</code>",
            quote=True,
        )

    # Check if custom URL site is passed before CC
    site = "shoepalace.com"
    parts = text.split()
    for part in parts:
        if "." in part and not part.replace("|", "").isdigit():
            site = part
            if not site.startswith("http"):
                site = "https://" + site
            break

    cc = ccs[0]
    mes = ccs[1]
    ano = ccs[2]
    cvv = ccs[3]

    antispam_result = antispam(user_id, user_info["ANTISPAM"], is_free_user)
    if antispam_result != False:
        return await m.reply(
            f"لطفا شکیبا باشید... -» <code>{antispam_result} ثانیه</code>", quote=True
        )

    msg_to_edit = await m.reply("لطفا شکیبا باشید در حال بررسی...", quote=True)

    try:
        response = await autoshopify(site, cc, mes, ano, cvv, is_premium, credits)
    except Exception as e:
        traceback.print_exc()
        return await msg_to_edit.edit(f"<b>خطا در پردازش درگاه! (<code>{type(e).__name__}: {str(e)[:100]}</code>)</b>")


    if not response or not isinstance(response, dict):
        return await msg_to_edit.edit("<b>پاسخی از درگاه دریافت نشد!</b>")

    response_gate = response.get("response", "نامشخص")
    status = response.get("status", "نامشخص")
    total_price = response.get("total", "1.00")
    t_time = response.get("time", "0.0")

    cc_formatted = f"{cc}|{mes}|{ano}|{cvv}"

    result_text = f"""<b>🔹 کارت -» <code>{cc_formatted}</code>
🔹 وضعیت -» <code>{status}</code>
🔹 نتیجه -» <code>{response_gate}</code>

🔹 درگاه -» <code>Shopify Auto ({site}) -» ${total_price[:5]}</code>
🔹 زمان -» <code>{t_time} ثانیه</code>
🔹 بررسی شده توسط -» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a></b>"""

    with Database() as db:
        db.increase_checks(user_id)

    await msg_to_edit.edit(result_text, disable_web_page_preview=True)
