#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telebot.types import CallbackQuery
from telebot import asyncio_filters

import asyncio
from admin_menu.admin_menu import ADMIN_FUNC_DICT
from bot_logic.anime_to_user import add_anime_in_list, change_buttons_add_new
from bot_logic.delete_user_anime import change_buttons_delete, delete_anime
from bot_logic.find_button import find_anime, get_find_list_anime
from bot_logic.ongoing_list import send_ong_chose, send_ongoing_list
from bot_logic.other_func import back_callback, close, start
from bot_logic.search_link import change_search_site
from bot_logic.show_button import start_show_list_anime
from bot_logic.user_push import delete_all_push_mes, send_anime_today_message
from push_func.push_while_true import find_new_anime_today
from classes.user_info import QueryUserInfo
from classes.message import MessageDeleteId
from classes.analitic import AnaliticClickData
from classes.error_decorator import ChangeSubscription
from config.bot_token import bot, id_list


# ~~~~~~~~~~~~~~~~~~~~~ admin callback functions ~~~~~~~~~~~~~~~~~~~~~


@bot.message_handler(
    commands=["admin"],
    content_types=["text"],
    func=lambda callback: callback.from_user.id in id_list,
)
@bot.callback_query_handler(
    func=lambda callback: callback.from_user.id in id_list
    and callback.data.split("#")[0] == "admin"
)
async def admin_call(call: CallbackQuery) -> None:
    try:
        func = ADMIN_FUNC_DICT.get(call.data.split("|||")[0], close)

    except AttributeError:
        func = ADMIN_FUNC_DICT.get(call.text, close)

    await func(call)


# ~~~~~~~~~~~~~~~~~~~~~ callback functions ~~~~~~~~~~~~~~~~~~~~~
@bot.message_handler(commands=["start"], content_types=["text"])
@bot.callback_query_handler(func=lambda callback: True)
@AnaliticClickData
@ChangeSubscription
async def call_find(call: CallbackQuery) -> None:
    try:
        func = DICT_FUNC_WORK.get(call.data.split("#")[0], close)

    except AttributeError:
        func = DICT_FUNC_WORK.get(call.text, close)

    await func(call)


# ~~~~~~~~~~~~~~~~~~~~~ delete text message ~~~~~~~~~~~~~~~~~~~~~


@bot.message_handler()
async def delete_message(message: CallbackQuery) -> None:
    user_query = QueryUserInfo(message)
    user_info = user_query.get_user()

    message_delete = MessageDeleteId()
    await message_delete.safe_message_delete(user_info, message)

    return


# ~~~~~~~~~~~~~~~~~~~~~ dicts for buttons ~~~~~~~~~~~~~~~~~~~~~

DICT_FUNC_WORK = {
    "/start": start,
    "back": back_callback,
    # find buttons
    "find_anime": find_anime,
    "get_find_list_anime": get_find_list_anime,
    "change_search_site": change_search_site,
    # need add functions
    "find_new_series": send_anime_today_message,
    "delete_all_push_mes": delete_all_push_mes,
    # add buttons
    "change_buttons_add_new": change_buttons_add_new,
    "add_new": add_anime_in_list,
    # show buttons
    "show_all": start_show_list_anime,
    # delete buttons
    "delete_anime": delete_anime,
    "change_buttons_delete": change_buttons_delete,
    # recomendations list
    "send_ongoing_list": send_ongoing_list,
    "back_ongoing": send_ongoing_list,
    "send_ong_chose": send_ong_chose,
    # navigations buttons
    "back_page|||show": start_show_list_anime,
    "next_page|||show": start_show_list_anime,
    "back_page|||change_delete": change_buttons_delete,
    "next_page|||change_delete": change_buttons_delete,
    "back_page|||delete": delete_anime,
    "next_page|||delete": delete_anime,
    "back_page|||find": get_find_list_anime,
    "next_page|||find": get_find_list_anime,
    "back_page|||change_add": change_buttons_add_new,
    "next_page|||change_add": change_buttons_add_new,
    "back_page|||add": add_anime_in_list,
    "next_page|||add": add_anime_in_list,
    "back_page|||find_new_series": send_anime_today_message,
    "next_page|||find_new_series": send_anime_today_message,
    "next_page|||ongoing": send_ong_chose,
    "back_page|||ongoing": send_ong_chose,
}


async def main():
    futures = [bot.polling(none_stop=True, interval=0), find_new_anime_today()]
    await asyncio.gather(*futures)


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(main())
