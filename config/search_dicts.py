#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 🏳🇷🇺🏳

SITE_FLAG = {
    "anitube": " 🇺🇦Anitube🇺🇦 ",
    "animego": " 🏳AnimeGo🏳 ",
    "hdrezka": " 🇺🇦HDrezka 🇺🇦",
}


BT_DICT = {
    f"{SITE_FLAG['animego']}": "change_search_site#animego",
    f"{SITE_FLAG['anitube']}": "change_search_site#anitube",
    f"{SITE_FLAG['hdrezka']}": "change_search_site#hdrezka",
    "Back": "back",
}


SEARCH_SITE_DICT = {
    "animego": {"link": "https://animego.org", "page_list": ""},
    "anitube": {"link": "https://anitube.in.ua/anime/", "page_list": "page/"},
    "hdrezka": {"link": "https://rezka.ag/", "page_list": ""},
}


SEARCH_SITE_INFO_DICT = {
    "animego": {
        "link": "https://animego.org/search/anime?q=",
        "page_list": "&type=list&page=",
        "stop_parse": ".alert-warning",
        "select": ".animes-grid-item",
    },
    "anitube": {
        "link": "https://anitube.in.ua/f/l.title=",
        "page_list": "/sort=date/order=desc/page/",
        "stop_parse": ".info_c",
        "select": ".story",
    },
    "hdrezka": {
        "link": "https://rezka.ag/search/?do=search&subaction=search&q=",
        "page_list": "&page=",
        "stop_parse": ".b-info__message",
        "select": ".b-content__inline_item",
    },
}


ONGOING_LIST_FIND_DICT = {
    "animego": {
        "link": "https://animego.org/anime/status/ongoing",
        "page_list": "?sort=a.createdAt&direction=desc&type=animes&page=",
        "stop_parse": "",
        "select": "#anime-list-container",
        "Cookie": "",
        "Cookie_text": {" ": "anime"},
    },
    "anitube": {
        "link": "https://anitube.in.ua/",
        "page_list": "",
        "stop_parse": "first page",
        "select": ".portfolio_items",
        "Cookie": "",
        "Cookie_text": {" ": "anime"},
    },
    "hdrezka": {
        "link": "https://rezka.ag",
        "page_list": "",
        "stop_parse": "82",
        "select": ".b-newest_slider__list",
        "Cookie": "newest_tab=",
        "Cookie_text": {"1": "movies", "2": "tvshow", "3": "cartoons", "82": "anime"},
    },
}


SEARCH_TAGS_TODAY_DICT = {
    "animego": {"find_soup": "#slide-toggle-1"},
    "anitube": {"find_soup": "#dle-content"},
    "hdrezka": {"find_soup": ".b-seriesupdate__block_list"},
}


# FOLDERS_CREATE_DICT = {
#     "./": ["save_image", "report_file"],
#     "./save_image/": ["animego", "anitube", "hdrezka"],
# }

FOLDERS_CREATE_DICT = {
    "/home/diosvolk/": ["save_data"],
    "/home/diosvolk/save_data/": ["image_list", "report_file"],
    "/home/diosvolk/save_data/image_list/": ["animego", "anitube", "hdrezka"],
}
