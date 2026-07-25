from pyrogram import filters
from pyromod import Client
from pyrogram.types import CallbackQuery
from utilsdf.cmds_desing import (
    text_home,
    buttons_cmds,
    buttons_gates,
    text_gates_auth,
    text_gates_auth_2,
    buttons_auth_page_1,
    buttons_auth_page_2,
    text_gates_charged,
    text_gates_charged_2,
    text_gates_charged_3,
    buttons_charged_page_1,
    buttons_charged_page_2,
    buttons_charged_page_3,
    text_gates_especials,
    buttons_specials_page_1,
    text_tools,
    text_tools_2,
    buttons_tools_page_1,
    buttons_tools_page_2,
)


@Client.on_callback_query(filters.regex("^home$"))
async def handler_home(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.edit_message_text(
        text=text_home.format(user_id),
        reply_markup=buttons_cmds,
    )


@Client.on_callback_query(filters.regex("^gates$"))
async def handler_gates(client: Client, callback_query: CallbackQuery):
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

    await callback_query.edit_message_text(
        f"""
<b>منوی درگاه‌ها »</b>

مجموع درگاه‌ها -» <code>{total}</code>
فعال -» <code>{gates_on} ✅</code>
غیرفعال -» <code>{gates_off} ❌</code>
<code>نوع درگاه مورد نظر خود را انتخاب کنید!</code>""",
        reply_markup=buttons_gates,
    )



@Client.on_callback_query(filters.regex("^auths(_2)?$"))
async def handler_auths(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "auths":
        await callback_query.edit_message_text(
            text_gates_auth, reply_markup=buttons_auth_page_1
        )
    elif callback_query.data == "auths_2":
        await callback_query.edit_message_text(
            text_gates_auth_2, reply_markup=buttons_auth_page_2
        )


@Client.on_callback_query(filters.regex("^chargeds(_[2-3])?$"))
async def handler_chargeds(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "chargeds":
        await callback_query.edit_message_text(
            text_gates_charged, reply_markup=buttons_charged_page_1
        )
    elif callback_query.data == "chargeds_2":
        await callback_query.edit_message_text(
            text_gates_charged_2, reply_markup=buttons_charged_page_2
        )
    elif callback_query.data == "chargeds_3":
        await callback_query.edit_message_text(
            text_gates_charged_3, reply_markup=buttons_charged_page_3
        )


@Client.on_callback_query(filters.regex("^specials$"))
async def handler_specials(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        text_gates_especials, reply_markup=buttons_specials_page_1
    )


@Client.on_callback_query(filters.regex("^tools(_2)?$"))
async def handler_tools(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "tools":
        await callback_query.edit_message_text(
            text_tools, reply_markup=buttons_tools_page_1
        )
    elif callback_query.data == "tools_2":
        await callback_query.edit_message_text(
            text_tools_2, reply_markup=buttons_tools_page_2
        )


@Client.on_callback_query(filters.regex("^exit$"))
async def handler_exit(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
