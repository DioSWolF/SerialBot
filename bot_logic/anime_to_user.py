#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
from bot_logic.find_button import get_find_list_anime
from buttons_create import (
    anime_butoons_create,
    create_image_text_message,
    create_special_buttons,
)
from classes.bot_query import AnimeToUser, PaginFindAnime, QueryAnime
from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery


# ~~~~~~~~~~~~~~~~~~~~~ add anime to user list ~~~~~~~~~~~~~~~~~~~~~


async def change_buttons_add_new(call: CallbackQuery) -> None:
    """
    Coroutine to handle the 'add_new' button when searching for anime.

    :param call: telebot.types.CallbackQuery - CallbackQuery object.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    pagin_anime = PaginFindAnime()
    message_delete = MessageDeleteId()

    user_info = user_query.get_user()

    await message_delete.delete_message_list(user_info)

    anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)
    anime_list = pagin_anime.get_anime_list(user_info)
    dump_num = pagin_anime.dump_num(call, user_info, anime_pagin_dict)

    #!!!
    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], callback="add_new")

    spec_dict = {"Back": "get_find_list_anime", "Search again": "find_anime"}
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||change_add",
            "Next page": "next_page|||change_add",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])

    edit_text = f"{user_info.user_name}-san, I have found {len(anime_list)} anime for you!\n\nClick to add series to your anime list\nPage №{dump_num + 1}/{len(anime_pagin_dict)}"
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


async def add_anime_in_list(call: CallbackQuery) -> None:
    """
    This function add_anime_in_list is responsible for adding selected anime to the user's list.

    :param call: The CallbackQuery object associated with the button press.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    message_delete = MessageDeleteId()
    pagin_anime = PaginFindAnime()
    user_to_anime = AnimeToUser()
    query_anime = QueryAnime()

    user_info = user_query.get_user()

    anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)
    dump_num = pagin_anime.dump_num(call, user_info, anime_pagin_dict)

    try:
        anime_index = int(call.data.split("#")[1])
        anime = anime_pagin_dict[dump_num][anime_index]
        user_to_anime.add_anime_user(user_info, anime)
        pagin_anime.del_anime_in_pagin(user_info, anime)

    except IndexError:
        pass

    anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)

    if dump_num >= len(anime_pagin_dict):
        dump_num = pagin_anime.dump_num(call, user_info, anime_pagin_dict)

    if len(anime_pagin_dict) == 0:
        await message_delete.delete_message_list(user_info)
        await query_anime.find_random_anime(message, user_info)

        anime_list = pagin_anime.get_anime_list(user_info)
        anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)

        return await get_find_list_anime(message, callback=call)
    #!!!
    spec_dict = {"Back": "get_find_list_anime", "Search again": "find_anime"}
    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], callback="add_new")
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {"Previous page": "back_page|||add", "Next page": "next_page|||add"}
        keyboard = create_special_buttons(keyboard, navig_bt)

    anime_list = pagin_anime.get_anime_list(user_info)
    await message_delete.delete_message_list(user_info)

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])

    # edit_text = f"{user_info.user_name.value}-san, I have found {len(ANIME_FIND_DICT[user_info.chat_id])} anime for you!\n\n{''.join(anime_list)}Click to add series to your anime list\nPage №{DICT_NUM_FIND[user_info.chat_id] + 1}/{len(FIND_ANIME_DICT_PAGINATION[user_info.chat_id])}"
    edit_text = f"{user_info.user_name}-san, I have found {len(anime_list)} anime for you!\n\nClick to add series to your anime list\nPage №{dump_num + 1}/{len(anime_pagin_dict)}"
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
