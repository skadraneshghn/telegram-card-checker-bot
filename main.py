import sys
import os
import time
import logging
from os import getenv

# Register sys.modules['main'] so plugins doing 'from main import ...' don't re-run main.py
if __name__ == "__main__":
    sys.modules["main"] = sys.modules[__name__]

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utilsdf.logger import logger
from web_server import start_web_server, set_config_error

logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Validate credentials safely
raw_api_id = getenv('TELEGRAM_API_ID', '').strip()
raw_api_hash = getenv('TELEGRAM_API_HASH', '').strip()
raw_bot_token = getenv('TELEGRAM_BOT_TOKEN', '').strip()
CHANNEL_LOGS = getenv('TELEGRAM_CHANNEL_LOGS', '')

missing_fields = []

if not raw_api_id or raw_api_id == 'YOUR_API_ID' or not raw_api_id.isdigit():
    missing_fields.append("TELEGRAM_API_ID")
    API_ID = 0
else:
    API_ID = int(raw_api_id)

if not raw_api_hash or raw_api_hash == 'YOUR_API_HASH':
    missing_fields.append("TELEGRAM_API_HASH")

if not raw_bot_token or raw_bot_token == 'YOUR_BOT_TOKEN':
    missing_fields.append("TELEGRAM_BOT_TOKEN")

from huepy import bad
from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import CallbackQuery, Message
from utilsdf.functions import bot_on
from utilsdf.db import Database
from utilsdf.vars import PREFIXES

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=raw_api_hash,
    bot_token=raw_bot_token,
    plugins=dict(root="plugins"),
    parse_mode=ParseMode.HTML,
)


@app.on_callback_query()
async def warn_user(client: Client, callback_query: CallbackQuery):
    if callback_query.message.reply_to_message.from_user and (
        callback_query.from_user.id
        != callback_query.message.reply_to_message.from_user.id
    ):
        await callback_query.answer("Usa tu menu! ⚠️", show_alert=True)
        return
    await callback_query.continue_propagation()


@app.on_message(filters.text)
async def user_ban(client: Client, m: Message):

    if not m.from_user:
        return
    if not m.text:
        return
    try:
        if not m.text[0] in PREFIXES:
            return
    except UnicodeDecodeError:
        return
    chat_id = m.chat.id
    with Database() as db:
        if chat_id == -1001494650944:
            async for member in m.chat.get_members():
                if not member.user:
                    continue
                if member.status == ChatMemberStatus.ADMINISTRATOR:
                    continue
                user_id = member.user.id
                if db.is_seller_or_admin(user_id):
                    continue
                is_premium = db.is_premium(user_id)
                if is_premium:
                    continue
                if db.user_has_credits(user_id):
                    continue
                await m.chat.ban_member(user_id)
                info = db.get_info_user(user_id)
                await client.send_message(-1001494650944, f"<b>User eliminado: @{info['USERNAME']}</b>")

        user_id = m.from_user.id
        username = m.from_user.username
        db.remove_expireds_users()
        banned = db.is_ban(user_id)
        if banned:
            return
        db.register_user(user_id, username)
        await m.continue_propagation()


if __name__ == "__main__":
    logger.info("Initializing Telegram Card Checker Bot...")
    start_web_server()

    if missing_fields:
        err_msg = f"Missing or invalid environment variables: {', '.join(missing_fields)}. Please configure them in your Clever Cloud Environment Variables dashboard."
        logger.warning("=" * 60)
        logger.warning("⚠️  " + err_msg)
        logger.warning("Web health check server on port 8080 will stay alive so Clever Cloud deployment succeeds.")
        logger.warning("=" * 60)
        set_config_error(err_msg)
        while True:
            time.sleep(10)
    else:
        bot_on()
        logger.info("Starting Pyrogram bot client and listening for Telegram updates...")
        app.run()
