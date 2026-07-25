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
    random_proxy,
)
from gates.CarolinaPayflow import payflowGate
from utilsdf.vars import PREFIXES
from time import perf_counter
from httpx import AsyncClient


@Client.on_message(filters.command(["it", "itachi"], PREFIXES))

async def itachi_cmd(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_premium(user_id):
            await user_not_premium(m)
            return
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
            """𝙂𝙖𝙩𝙚𝙬𝙖𝙮 <code>𝙄𝙩𝙖𝙘𝙝𝙞 ♻️</code>
𝙁𝙤𝙧𝙢𝙖𝙩 -» <code>/it cc|month|year|cvc</code>""",
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

    async with AsyncClient(
        follow_redirects=True, verify=False, proxies=random_proxy()
    ) as s:
        try:
            msj, cvcode, avscode = await payflowGate(ccs[0], ccs[1], ccs[2], ccs[3], s)
        except BaseException as e:
            msj, avscode, cvcode = "Error! ⚠️", "Error! ⚠️", "Error! ⚠️"
            print(e)
        finally:
            await s.aclose()
    if "Verified" in msj:
        status = "Approved! ✅"
    elif "CVV2 Mismatch" in msj:
        status = "Approved! ✅ -» ccn"
    elif "funds" in msj:
        status = "Approved! ✅ -» low funds"
    else:
        status = "Dead! ❌"

    final = perf_counter() - ini
    with Database() as db:
        db.increase_checks(user_id)

    text_ = f"""<b>ア 𝘾𝘾 -» <code>{cc_formatted}</code>
カ 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{status}</code>
ツ 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{msj}</code>
ツ 𝘾𝙫𝙘 -» <code>{cvcode}</code> -  𝘼𝙫𝙨 -» <code>{avscode}</code>

キ 𝘽𝙞𝙣 -» <code></code> - <code></code> - <code></code>
🔹 𝘽𝙖𝙣𝙠 -» <code></code>
🔹 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code></code> 

⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>𝙄𝙩𝙖𝙘𝙝𝙞 ♻️</code>
꫟ 𝙏𝙞𝙢𝙚 -» <code>{final:0.3}'s</code>
ᥫ᭡ 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> []</b>"""

    await msg.edit(text_)
