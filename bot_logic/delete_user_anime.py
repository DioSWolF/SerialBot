#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This module provides functions for deleting anime from a user's list.

"""


# ~~~~~~~~~~~~~~~~~~~~~ delete anime in my list ~~~~~~~~~~~~~~~~~~~~~


import asyncio
from bot_logic.other_func import back_callback
from buttons_create import (
    anime_butoons_create,
    create_image_text_message,
    create_special_buttons,
)
from classes.bot_query import AnimeToUser, ShowUserList
from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery


async def change_buttons_delete(call: CallbackQuery) -> None:
    """
    This function updates the list of anime that a user can delete and sends it as a new message.

    :param call: CallbackQuery object that contains information about the button pressed.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    show_user_anime_query = ShowUserList()
    message_delete = MessageDeleteId()

    user_info = user_query.get_user()

    await message_delete.delete_message_list(user_info)

    anime_list = show_user_anime_query.get_anime_list(user_info)
    anime_pagin_dict = show_user_anime_query.get_pagin_anime_dict(user_info)

    dump_num = show_user_anime_query.dump_num(call, user_info, anime_pagin_dict)
    #!!!
    spec_dict = {
        "Back": "show_all",
        "Search for new anime": "find_anime",
    }
    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], callback="delete_anime")
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||change_delete",
            "Next page": "next_page|||change_delete",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    edit_text = f"{user_info.user_name}-san, you have {len(anime_list)} anime.\n\nClick to delete series from your anime list\nPage №{dump_num + 1}/{len(anime_pagin_dict)}"

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])
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


# delete anime


async def delete_anime(call: CallbackQuery) -> None:
    """
    This function deletes an anime from a user's list and updates the list.

    :param call: CallbackQuery object that contains information about the button pressed.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    show_user_anime_query = ShowUserList()
    message_delete = MessageDeleteId()
    user_to_anime = AnimeToUser()

    user_info = user_query.get_user()

    anime_list = show_user_anime_query.get_anime_list(user_info)
    anime_pagin_dict = show_user_anime_query.get_pagin_anime_dict(user_info)
    dump_num = show_user_anime_query.dump_num(call, user_info, anime_pagin_dict)

    try:
        anime_index = int(call.data.split("#")[1])
        anime = anime_pagin_dict[dump_num][anime_index]
        user_to_anime.del_anime_user(user_info, anime)

    except IndexError:
        pass

    anime_pagin_dict = show_user_anime_query.get_pagin_anime_dict(user_info)
    anime_list = show_user_anime_query.get_anime_list(user_info)
    if dump_num >= len(anime_pagin_dict):
        dump_num = show_user_anime_query.dump_num(call, user_info, anime_pagin_dict)

    if len(anime_pagin_dict) == 0:
        return await back_callback(call)

    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], callback="delete_anime")
    spec_dict = {"Back": "show_all", "Search for new anime": "find_anime"}
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||delete",
            "Next page": "next_page|||delete",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    edit_text = f"{user_info.user_name}-san, you have {len(anime_list)} anime.\n\nClick to delete series from your anime list\nPage №{dump_num + 1}/ {len(anime_pagin_dict)}"
    # ^^^
    await message_delete.delete_message_list(user_info)

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])

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
