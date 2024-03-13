#!/usr/bin/env python
# -*- coding: utf-8 -*-


from buttons_create import anime_today_buttons, create_special_buttons
from classes.message import MessageDeleteId
from classes.push_query import QueryAnimeToday
from classes.user_info import QueryUserInfo
from config.bot_token import bot
from telebot.types import CallbackQuery


async def send_anime_today_message(call: CallbackQuery) -> None:
    """
    Sends a message to the user with the anime episodes scheduled for today.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    user_query = QueryUserInfo(message)
    message_delete = MessageDeleteId()
    animetoday_query = QueryAnimeToday()

    user_info = user_query.get_user()
    anime_list = animetoday_query.all_records_today(user_info)
    animetoday_query.add_num_pagin(user_info)
    anime_pagin_dict = animetoday_query.get_pagin_dict()

    if len(anime_list) < 1:
        return

    await message_delete.del_pg_save_mes(user_info)
    #!!!

    dump_num = animetoday_query.dump_num(call, user_info, anime_pagin_dict)

    keyboard, message_text = anime_today_buttons(anime_pagin_dict[dump_num])

    if len(anime_pagin_dict) > 1:
        navig_bt = {
            "Previous page": "back_page|||find_new_series",
            "Next page": "next_page|||find_new_series",
        }
        keyboard = create_special_buttons(keyboard, navig_bt)

    del_bt = {"Delete message": "delete_all_push_mes"}
    keyboard = create_special_buttons(keyboard, del_bt)

    edit_text = f"{user_info.user_name}-san, you have {len(anime_list)} new episodes.\n\n{''.join(message_text)}Page №{dump_num + 1}/{len(anime_pagin_dict)}"
    # ^^^
    mes_id = await bot.send_message(user_info.user_id, edit_text, reply_markup=keyboard)

    message_delete.add_save_pg_mes_id(user_info, mes_id)
    # message_delete.add_pagin_mes_id(user_info, mes_id)
    return


async def delete_all_push_mes(call: CallbackQuery) -> None:
    """
    Asynchronously deletes all pagination messages related to the user who triggered the callback query.

    :param call: The callback query sent by the user.
    :type call: CallbackQuery

    :return: None
    :rtype: None
    """

    message = call.message

    message_delete = MessageDeleteId()
    user_query = QueryUserInfo(message)

    user_info = user_query.get_user()

    await message_delete.delete_pagin_mes_list(user_info, message)

    return
