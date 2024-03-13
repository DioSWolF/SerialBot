#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This script sends a message to the user with ongoing anime recommendations, 
allowing them to choose a type of recommendation to see a list of specific anime. 
"""


import asyncio
from buttons_create import (
    anime_butoons_create,
    create_image_text_message,
    create_special_buttons,
    one_type_buttons_create,
)
from classes.bot_query import PaginFindAnime
from classes.message import MessageDeleteId
from classes.ongoing_query import QueryOngoing
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery


# ~~~~~~~~~~~~~~~~~~~~~ send ongoing list today to user ~~~~~~~~~~~~~~~~~~~~~


async def send_ongoing_list(call: CallbackQuery) -> None:
    """
    Sends the initial message with the list of ongoing anime recommendation types to choose from.

    :param call: CallbackQuery object containing the user's callback query data.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    message_delete = MessageDeleteId()

    user_info = user_query.get_user()

    ong_user = QueryOngoing(user_info, call)

    ong_user.clean_pagin()
    bt_dict = ONGOING_BUTTONS_DICT[user_info.chose_site]

    if len(bt_dict) <= 1:
        call.data = "send_ong_chose#anime"
        return await send_ong_chose(call)

    await message_delete.delete_message_list(user_info)
    keyboard = one_type_buttons_create(bt_dict, 2)

    keyboard = create_special_buttons(keyboard, {"Back": "back"})

    edit_text = "Choose recommended type"

    await message_delete.safe_message_delete(user_info, message)

    await bot.send_message(
        chat_id=user_info.user_id, text=edit_text, reply_markup=keyboard
    )


async def send_ong_chose(call: CallbackQuery) -> None:
    """
    Sends the message with the list of specific anime for the chosen recommendation type.

    :param call: CallbackQuery object containing the user's callback query data.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    message_delete = MessageDeleteId()
    pagin_anime = PaginFindAnime()

    user_info = user_query.get_user()
    ong_user = QueryOngoing(user_info, call)

    bt_dict = ONGOING_BUTTONS_DICT[user_info.chose_site]

    if call.data in bt_dict.values():
        ong_user.get_ongoing_list()

        if ong_user.ong_list == []:
            return

    await message_delete.safe_message_delete(user_info, message)
    await message_delete.delete_message_list(user_info)

    anime_pagin_dict = pagin_anime.get_pagin_anime_dict(user_info)

    pagin_anime.add_num_pagin(user_info)
    dump_num = pagin_anime.dump_num(call, user_info, anime_pagin_dict)

    anime_list = pagin_anime.get_anime_list(user_info)

    keyboard = anime_butoons_create(anime_pagin_dict[dump_num], url="")

    back_bt = "back_ongoing"

    if len(bt_dict) <= 1:
        back_bt = "back"

    spec_dict = {
        "Back": back_bt,
        "Add series to your anime list": "change_buttons_add_new",
    }

    keyboard = create_special_buttons(keyboard, spec_dict)

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": f"back_page|||ongoing",
            "Next page": f"next_page|||ongoing",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    image_text_message = await create_image_text_message(anime_pagin_dict[dump_num])

    edit_text = f"{user_info.user_name}-san, I have found {len(anime_list)} anime for you!\n\nClick the button to open anime on website\nPage №{dump_num + 1}/{len(anime_pagin_dict)}"

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


ONGOING_BUTTONS_DICT = {
    "animego": {"Anime": "send_ong_chose#anime"},
    "anitube": {"Anime": "send_ong_chose#anime"},
    "hdrezka": {
        "Anime": "send_ong_chose#anime",
        "Movies": "send_ong_chose#movies",
        "TV show": "send_ong_chose#tvshow",
        "Cartoons": "send_ong_chose#cartoons",
    },
}
