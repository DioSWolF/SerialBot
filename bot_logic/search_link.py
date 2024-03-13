#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This module contains a function to handle changing the search site for the bot user.
"""

from buttons_create import one_type_buttons_create
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery

from config.search_dicts import BT_DICT, SITE_FLAG


async def change_search_site(call: CallbackQuery) -> None:
    """
    Asynchronously change the search site of a user.

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

    if len(call.data.split("#")) >= 2:
        user_query.change_user_site(call.data.split("#")[1])
        user_info = user_query.get_user()

    edit_text = (
        f"You have chosen site: {SITE_FLAG[user_info.chose_site]}\nChange anime source?"
    )

    keyboard = one_type_buttons_create(BT_DICT, 1)

    await bot.edit_message_text(
        edit_text,
        chat_id=user_info.chat_id,
        message_id=message.id,
        reply_markup=keyboard,
    )
