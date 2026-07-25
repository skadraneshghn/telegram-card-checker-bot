from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.cmds_desing import (
    text_home,
    buttons_cmds,
    buttons_gates,
    text_gates_auth,
    text_gates_auth_2,
    text_gates_charged,
    text_gates_charged_2,
    text_gates_charged_3,
    text_gates_especials,
)
from utilsdf.vars import PREFIXES


@Client.on_message(filters.command(["start", "iniciar", "inicio"], PREFIXES))
async def start_cmd(client: Client, m: Message):
    user_id = m.from_user.id
    await m.reply_text(
        text=text_home.format(user_id),
        reply_markup=buttons_cmds,
        quote=True,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["cmds", "cmd", "help", "menu", "gates", "gate"], PREFIXES))
async def cmds(client: Client, m: Message):
    all_gates_text = (
        text_gates_auth
        + text_gates_auth_2
        + text_gates_charged
        + text_gates_charged_2
        + text_gates_charged_3
        + text_gates_especials
    )

    gates_on = all_gates_text.count("✅")
    gates_off = all_gates_text.count("❌")
    gates_mantenience = all_gates_text.count("⚠️")
    total = gates_on + gates_off + gates_mantenience

    text = f"""<b>📋 لیست دستورات و درگاه‌های ربات »</b>

مجموع درگاه‌ها -» <code>{total}</code>
فعال -» <code>{gates_on} ✅</code>
غیرفعال -» <code>{gates_off} ❌</code>

<code>لطفا دسته‌بندی درگاه یا ابزار مورد نظر خود را انتخاب کنید:</code>"""

    await m.reply_text(
        text=text,
        reply_markup=buttons_gates,
        quote=True,
        disable_web_page_preview=True,
    )
