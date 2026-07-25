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
)
from utilsdf.vars import PREFIXES
from gates.pp import pp_gate
from time import perf_counter

price = "$0.01"


@Client.on_message(filters.command("pp", PREFIXES))
async def pp_cmd(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_authorized(user_id, m.chat.id):
            return await m.reply(
                "𝑻𝒉𝒊𝒔 𝒄𝒉𝒂𝒕 𝒊𝒔 𝒏𝒐𝒕 𝒂𝒑𝒑𝒓𝒐𝒗𝒆𝒅 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.", quote=True
            )
        user_info = db.get_info_user(user_id)
        is_free_user = user_info["MEMBERSHIP"]
        is_free_user = is_free_user.lower() == "free user"
        if is_free_user:
            captcha = await anti_bots_telegram(m, client)
            if not captcha:
                return
    text = get_text_from_pyrogram(m)
    ccs = get_cc(text)
    if not ccs:
        return await m.reply(
            f"𝙂𝙖𝙩𝙚𝙬𝙖𝙮 <code>𝙋𝙖𝙮𝙋𝙖𝙡 ♻️ -» {price}</code>\n𝙁𝙤𝙧𝙢𝙖𝙩 -» <code>/pp cc|month|year|cvc</code>",
            quote=True,
        )
    ini = perf_counter()
    cc = ccs[0]
    mes = ccs[1]
    ano = ccs[2]
    cvv = ccs[3]

    
    # check antispam
    antispam_result = antispam(user_id, user_info["ANTISPAM"], is_free_user)
    if antispam_result != False:
        return await m.reply(
            f"𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩... -» <code>{antispam_result}'s</code>", quote=True
        )
    msg = await m.reply("𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩...", quote=True)
    cc_formatted = f"{cc}|{mes}|{ano}|{cvv}"

    message_error, code_error = await pp_gate(cc, mes, ano, cvv)
    response_to_check = message_error.lower()
    status = "Dead! ❌"
    status1 = f"{code_error} -» {message_error}"
    if "is3DSecureRequired" in message_error:
        status = "Approved! ✅ -» charged!"
        status1 = f"Success -» {price}"
    if "PAYER_CANNOT_PAY" in response_to_check:
        status = "Approved! ✅ -» charged!"
        status1 = f"Success -» {price}"
    elif "ADD_SHIPPING_ERROR" in response_to_check:
        status = "Approved! ✅ -» charged!"
        status1 = f"Success -» {price} -» ¿?"
    elif "EXISTING_ACCOUNT_RESTRICTED" in code_error:
        status = "Approved! ✅ -» #auth"
        status1 = "EXISTING_ACCOUNT_RESTRICTED"
    elif "INVALID_BILLING_ADDRESS" in code_error:
        status = "Approved! ✅ -» avs"
        status1 = code_error
    elif "INVALID_SECURITY_CODE" in code_error:
        status = "Approved! ✅ -» ccn"
        status1 = code_error
    elif "VALIDATION_ERROR" in code_error:
        status = "Approved! ✅ -» ccn"
        status1 = "VALIDATION_ERROR"

    final = perf_counter() - ini
    with Database() as db:
        db.increase_checks(user_id)

    text_ = f"""<b>ア 𝘾𝘾 -» <code>{cc_formatted}</code>
カ 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{status}</code>
ツ 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{status1}</code>

キ 𝘽𝙞𝙣 -» <code></code> - <code></code> - <code></code>
🔹 𝘽𝙖𝙣𝙠 -» <code></code>
🔹 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code></code> 

⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>𝙋𝙖𝙮𝙋𝙖𝙡 -» {price}</code>
꫟ 𝙏𝙞𝙢𝙚 -» <code>{final:0.3}'s</code>
ᥫ᭡ 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> []</b>"""

    await msg.edit(text_)
