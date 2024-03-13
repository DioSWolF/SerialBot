#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ~~~~~~~~~~~~~~~~~~~~~ show list ~~~~~~~~~~~~~~~~~~~~~


import asyncio
from buttons_create import (
    anime_butoons_create,
    create_image_text_message,
    create_special_buttons,
)
from classes.bot_query import ShowUserList
from classes.message import MessageDeleteId
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery


async def start_show_list_anime(call: CallbackQuery) -> None:
    """
    Start the process of showing the user's anime list.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    message_delete = MessageDeleteId()
    show_user_anime_query = ShowUserList()

    user_info = user_query.get_user()
    show_user_anime_query.add_pagin_num(user_info)
    anime_list = show_user_anime_query.get_anime_list(user_info)

    if len(anime_list) == 0:
        return

    await message_delete.delete_message_list(user_info)

    anime_pagin_dict = show_user_anime_query.get_pagin_anime_dict(user_info)

    dump_num = show_user_anime_query.dump_num(call, user_info, anime_pagin_dict)
    #!!!
    spec_dict = {
        "Back": "back",
        "Delete series from your anime list": "change_buttons_delete",
        "Search for new anime": "find_anime",
    }
    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], url="")
    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||show",
            "Next page": "next_page|||show",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    edit_text = f"{user_info.user_name}-san, you have {len(anime_list)} anime.\n\nClick the button to open anime on website\n Page №{dump_num + 1}/{len(anime_pagin_dict)}"

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
