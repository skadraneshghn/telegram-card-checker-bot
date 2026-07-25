from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.db import Database
from utilsdf.functions import get_text_from_pyrogram, user_not_premium
from utilsdf.vars import PREFIXES
from gates.ssh import ssh
from time import perf_counter
import re


@Client.on_message(filters.command("ssh", PREFIXES))
async def ssh(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_admin(user_id):
            await user_not_premium(m)
            return
        user_info = db.get_info_user(user_id)
    text = get_text_from_pyrogram(m)
    e_ = re.split(r"\||\s|:", text)
    us = e_[1] if len(e_) > 1 else None
    ps = e_[2] if len(e_) > 2 else None
    s = e_[3] if len(e_) > 3 else None

    if us == None or ps == None or s == None:
        return await m.reply(
            "𝙂𝙖𝙩𝙚𝙬𝙖𝙮 <code>𝙎𝙨𝙝 ♻️</code>\n𝙁𝙤𝙧𝙢𝙖𝙩 -» <code>/ssh user password br 1</code>",
            quote=True,
        )
    ini = perf_counter()

    msg_to_edit = await m.reply("𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩...", quote=True)
    try:
        (
            status,
            msg,
            ip,
            host,
            us,
            ps,
            exp,
            limit,
            server,
            ssh_,
            ssl,
            websocket,
            direct,
            key_dns,
            ns_dns,
        ) = await ssh(us, ps, s)
    except Exception as e:
        return await msg_to_edit.edit(f"<b>Error: {type(e).__name__}</b>")


    final = perf_counter() - ini

    rol = user_info["RANK"].capitalize()

    await msg_to_edit.edit(
        f"""<b>カ 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{status}</code>
ツ 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{msg}</code>

ア 𝙃𝙤𝙨𝙩 -» <code>{host}</code>
ツ 𝙐𝙨𝙚𝙧 -» <code>{us}</code>
キ 𝙋𝙖𝙨𝙨 -» <code>{ps}</code>
🔹 𝙎𝙚𝙧𝙫𝙚𝙧 -» <code>{server}</code>

カ 𝙄𝙥 -» <code>{ip}</code>
🔹 𝙀𝙭𝙥 -» <code>{exp}</code>
ア 𝙇𝙞𝙢𝙞𝙩 -» <code>{limit}</code>

カ 𝙎𝙨𝙝 -» <code>{ssh_}</code>
ツ 𝙎𝙨𝙡 -» <code>{ssl}</code>
キ 𝙒𝙚𝙗𝙨𝙤𝙘𝙠𝙚𝙩 -» <code>{websocket}</code>
🔹 𝘿𝙞𝙧𝙚𝙘𝙩 -» <code>{direct}</code>
🔹 𝙆𝙚𝙮 𝘿𝙣𝙨 -» <code>{key_dns}</code>
ツ 𝙉𝙨 𝘿𝙣𝙨 -» <code>{ns_dns}</code>

⸙ 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>𝙎𝙨𝙝</code>
꫟ 𝙏𝙞𝙢𝙚 -» <code>{final:0.3}'s</code>
ᥫ᭡ 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> [{rol
    }]</b>"""
    )
