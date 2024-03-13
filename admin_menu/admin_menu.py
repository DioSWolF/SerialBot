#!/usr/bin/env python
# -*- coding: utf-8 -*-


import aiofiles
from admin_menu.analitic_query import AdminCleanTable, AnaliticInfo
from buttons_create import date_buttons, one_type_buttons_create
from classes.analitic import AnaliticUserData

from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from config.bot_token import bot, base_path
from telebot.types import CallbackQuery, Message


async def send_menu(call: CallbackQuery) -> None:
    """
    Send the main admin menu to the user.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    try:
        message: Message = call.message
    except AttributeError:
        message: Message = call

    user_query = QueryUserInfo(message)
    user_info = user_query.get_user()

    message_delete = MessageDeleteId()

    if user_query.user_info == None:
        user_query.add_new_user()
        user_info = user_query.get_user()

    keyboard = one_type_buttons_create(MENU_DICT, 1)

    edit_text = "admin menu"

    message_info = await bot.send_message(
        user_info.chat_id, edit_text, reply_markup=keyboard
    )

    message_delete.add_message_id(user_info, message_info)
    await message_delete.safe_message_delete(user_info, message)

    return


async def back_adm_menu(call: CallbackQuery):
    """Go back to the main admin menu.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    message_delete = MessageDeleteId()
    user_query = QueryUserInfo(message)

    user_info = user_query.get_user()

    await message_delete.safe_message_delete(user_info, message)

    keyboard = one_type_buttons_create(MENU_DICT, 1)
    edit_text = "Admin menu"

    await bot.send_message(user_info.chat_id, edit_text, reply_markup=keyboard)


async def clean_button(call: CallbackQuery):
    """
    Send the clean database menu to the user.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    message_delete = MessageDeleteId()
    user_query = QueryUserInfo(message)

    user_info = user_query.get_user()

    keyboard = one_type_buttons_create(CLEAN_DICT, 1)

    edit_text = "Clean database menu (use only development)"

    await message_delete.safe_message_delete(user_info, message)
    await bot.send_message(user_info.chat_id, edit_text, reply_markup=keyboard)


async def clean_database(call: CallbackQuery):
    """
    Clean the database table.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    func = CLEAN_FUNC_DICT.get(call.data)
    user_query = QueryUserInfo(message)

    user_info = user_query.get_user()

    await func(call)

    for text, keys in CLEAN_DICT.items():
        if call.data == keys:
            edit_text = text

    await bot.send_message(chat_id=user_info.user_id, text=edit_text)


async def all_info_xmlx(call):
    """
    Send the analytics report to the user.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    user_query = QueryUserInfo(message)
    month_info = AnaliticInfo()
    user_report = AnaliticUserData()

    user_info = user_query.get_user()

    user_report.create_month_data()
    await month_info.create_report_xmlx()

    await bot.send_document(
        user_info.user_id,
        document=month_info.file,
        visible_file_name="report_data.xlsx",
    )


async def info_month(call: CallbackQuery):
    """
    Send the date picker menu to the user to choose a month to display data.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    message_delete = MessageDeleteId()
    user_query = QueryUserInfo(message)
    month_info = AnaliticInfo()

    user_info = user_query.get_user()
    month_info.get_all_date()
    keyboard = date_buttons(month_info)

    await message_delete.safe_message_delete(user_info, message)
    await bot.send_message(
        chat_id=user_info.user_id, text="Chose date", reply_markup=keyboard
    )


async def send_data(call: CallbackQuery):
    """
    Sends the monthly report to the user who requested it.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    user_query = QueryUserInfo(message)
    month_info = AnaliticInfo()
    create_report = AnaliticUserData()

    user_info = user_query.get_user()
    create_report.create_month_data()
    month_info.get_month_all(call)

    await bot.send_message(chat_id=user_info.user_id, text=month_info.report_text)


async def send_database_file(call: CallbackQuery):
    """
    Sends the database file to the user who requested it.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message: Message = call.message

    user_query = QueryUserInfo(message)
    user_info = user_query.get_user()

    async with aiofiles.open(base_path, "rb") as file:
        file = await file.read()

    await bot.send_document(
        user_info.user_id, document=file, visible_file_name="anime_bd.db"
    )


"""
These dictionaries are used to route button callbacks to the appropriate functions.
"""


ADMIN_FUNC_DICT = {
    "/admin": send_menu,
    "admin#back": back_adm_menu,
    "admin#clean_button": clean_button,
    "admin#month_info": info_month,
    "admin#all_info_xmlx": all_info_xmlx,
    "admin#send_database_file": send_database_file,
    "admin#send_data": send_data,
    "admin#clean_database": clean_database,
}


CLEAN_FUNC_DICT = {
    "admin#clean_database|||clean_anime_today": AdminCleanTable().clean_anime_today,
    "admin#clean_database|||clean_user_push": AdminCleanTable().clean_user_push,
    "admin#clean_database|||clean_find_anime": AdminCleanTable().clean_find_anime,
    "admin#clean_database|||clean_anime": AdminCleanTable().clean_anime,
    "admin#clean_database|||clean_all_table": AdminCleanTable().clean_all_table,
}


# ~~~~~~~~~~~~~~~~~~~~~ buttons dict ~~~~~~~~~~~~~~~~~~~~~


MENU_DICT = {
    "Clean database": "admin#clean_button",
    "Month info": "admin#month_info",
    "All info xmlx": "admin#all_info_xmlx",
    "Send database file": "admin#send_database_file",
}


CLEAN_DICT = {
    "Clean list 'new today'": "admin#clean_database|||clean_anime_today",
    "Clean list 'user push'": "admin#clean_database|||clean_user_push",
    "Clean list 'find anime'": "admin#clean_database|||clean_find_anime",
    "Clean list 'all anime'": "admin#clean_database|||clean_anime",
    "Clean all tables": "admin#clean_database|||clean_all_table",
    "Back": "admin#back",
}
