#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This module contains functions and handlers for finding and listing anime.
"""


from buttons_create import (
    anime_butoons_create,
    create_image_text_message,
    create_special_buttons,
    one_type_buttons_create,
)
from classes.bot_query import PaginFindAnime, QueryAnime
from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from parse.find_anime import MyStates
from telebot.types import CallbackQuery
import asyncio
from config.bot_token import bot


# ~~~~~~~~~~~~~~~~~~~~~ find anime to user list ~~~~~~~~~~~~~~~~~~~~~


async def find_anime(call: CallbackQuery) -> None:
    """
    Handler function for finding an anime given by the user.

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
    edit_text = f"{user_info.user_name}-san, enter the name of the anime and I will find it for you!"
    keyboard = one_type_buttons_create(FUNC_BACK_DICT, 2)
    # ^
    await bot.set_state(user_info.user_id, MyStates.find_text, message.chat.id)
    await asyncio.sleep(0.5)

    await bot.edit_message_text(
        edit_text,
        chat_id=user_info.chat_id,
        message_id=message.id,
        reply_markup=keyboard,
    )

    return


# find and get anime list
@bot.message_handler(state=MyStates.find_text)
async def get_find_list_anime(
    call: CallbackQuery, callback: CallbackQuery = None
) -> None:
    """
    Handler function for getting a list of found anime and displaying it to the user.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :param callback: The callback query to use as reference for pagination, defaults to None.
    :type callback: CallbackQuery, optional

    :return: None
    :rtype: None
    """

    if type(call) == list:
        call = call[0]

    try:
        message = call.message
        call_data = call.data
    except AttributeError:
        message = call
        call_data = ""

    user_query = QueryUserInfo(message)
    query_anime = QueryAnime()
    pagin_anime = PaginFindAnime()
    message_delete = MessageDeleteId()

    user_info = user_query.get_user()

    await message_delete.delete_message_list(user_info)

    pagin_anime.add_num_pagin(user_info)

    try:
        anime_list = pagin_anime.get_anime_list(user_info)

    except KeyError:
        return

    if callback == None:
        callback = call

    if call_data == "":
        await query_anime.find_anime(message, user_info)

        anime_list = pagin_anime.get_anime_list(user_info)

        while len(anime_list) == 0:
            await query_anime.find_random_anime()
            anime_list = pagin_anime.get_anime_list(user_info)

    anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)
    dump_num = pagin_anime.dump_num(callback, user_info, anime_pagin_dict)

    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], url="")

    spec_dict = {
        "Back": "back",
        "Add series to your anime list": "change_buttons_add_new",
        "Search again": "find_anime",
    }
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||find",
            "Next page": "next_page|||find",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])

    edit_text = f"{user_info.user_name}-san, I have found {len(anime_list)} anime for you!\n\nClick the button to open anime on website\nPage №{dump_num + 1}/{len(anime_pagin_dict)}"
    # ^^^
    mes_id = await bot.send_media_group(
        chat_id=user_info.chat_id, media=image_text_message
    )
    message_delete.add_message_id(user_info, mes_id)

    await asyncio.sleep(0.5)

    mes_id = await bot.send_message(
        chat_id=user_info.chat_id, text=edit_text, reply_markup=keyboard
    )
    message_delete.add_message_id(user_info, mes_id)
    return


FUNC_BACK_DICT = {"Back": "back"}
