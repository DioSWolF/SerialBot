#!/usr/bin/env python
# -*- coding: utf-8 -*-


from buttons_create import contact_with_me, one_type_buttons_create
from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery

from config.search_dicts import SITE_FLAG


# ~~~~~~~~~~~~~~~~~~~~~ /start bot ~~~~~~~~~~~~~~~~~~~~~


async def start(call: CallbackQuery) -> None:
    """
    Function to start the chat with the user by sending the welcome message
    and the buttons to choose the desired action.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    try:
        message = call.message
    except AttributeError:
        message = call

    user_query = QueryUserInfo(message)
    user_info = user_query.get_user()

    message_delete = MessageDeleteId()

    if user_query.user_info == None:
        user_query.add_new_user()
        user_info = user_query.get_user()

    #!
    edit_text = f"\n{SITE_FLAG[user_info.chose_site]}Irasshaimase, {user_info.user_name}-san!{SITE_FLAG[user_info.chose_site]}"

    keyboard = one_type_buttons_create(DEF_DICT, 3)
    keyboard = contact_with_me(keyboard)

    message_info = await bot.send_message(
        user_info.chat_id, edit_text, reply_markup=keyboard
    )

    message_delete.add_message_id(user_info, message_info)
    await message_delete.safe_message_delete(user_info, message)

    return


# ~~~~~~~~~~~~~~~~~~~~~ back button ~~~~~~~~~~~~~~~~~~~~~


async def back_callback(call: CallbackQuery) -> None:
    """
    Function to go back to the previous screen by sending the
    previous message again with the same keyboard.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    try:
        message = call.message
    except AttributeError:
        message = call

    user_query = QueryUserInfo(message)
    user_info = user_query.get_user()

    message_delete = MessageDeleteId()
    await message_delete.special_delete(user_info, 0, -1)
    #!
    edit_text = f"\n{SITE_FLAG[user_info.chose_site]}Irasshaimase, {user_info.user_name}-san!{SITE_FLAG[user_info.chose_site]}"

    keyboard = one_type_buttons_create(DEF_DICT, 3)
    keyboard = contact_with_me(keyboard)
    # ^
    await bot.delete_state(user_info.user_id, user_info.chat_id)
    await bot.edit_message_text(
        edit_text,
        chat_id=user_info.chat_id,
        message_id=message.id,
        reply_markup=keyboard,
    )

    return


# ~~~~~~~~~~~~~~~~~~~~~ get close function ~~~~~~~~~~~~~~~~~~~~~


async def close(*_) -> None:
    """
    Function to close the current screen and do nothing.
    :param _: Arguments that are not used in the function

    :return: None
    :rtype: None
    """

    pass


DEF_DICT = {
    "Search anime": "find_anime",
    "Show my anime list": "show_all",
    "Show ongoing anime series": "find_new_series",
    "Change anime source": "change_search_site",
    "Recommendations list": "send_ongoing_list",
}
