#!/usr/bin/env python
# -*- coding: utf-8 -*-


from database.mymodels import AnimeDB, FindAnimeBD, OngoingBD, UserInfoDB
from telebot.types import CallbackQuery
from database.mymodels import session_db


class QueryOngoing:
    pagin_anime_model = FindAnimeBD
    user_info_model = UserInfoDB
    anime_model = AnimeDB
    ongoing_model = OngoingBD
    session = session_db

    def __init__(self, user_info: UserInfoDB, marker: CallbackQuery) -> None:
        self.search_key = user_info.chose_site
        self.user_info = user_info

        try:
            self.marker = marker.data.split("#")[1]

        except IndexError:
            self.marker = "first"

    def get_ongoing_list(self):
        self.find_anime()
        self.add_pagin_list()

    def find_anime(self):
        self.ong_list: list[AnimeDB] = (
            self.session.query(AnimeDB)
            .join(OngoingBD)
            .filter(
                AnimeDB.anime_site_link == self.search_key,
                OngoingBD.anime_id == AnimeDB.anime_id,
                OngoingBD.marker == self.marker,
            )
            .all()
        )

    def add_pagin_list(self):
        for anime in self.ong_list:
            pagin_anime = self.pagin_anime_model(
                user_id=self.user_info.user_id, anime_id=anime.anime_id
            )
            self.session.add(pagin_anime)
        self.session.commit()

    def clean_pagin(self):
        self.session.query(self.pagin_anime_model).filter_by(
            user_id=self.user_info.user_id
        ).delete()
        self.session.commit()
