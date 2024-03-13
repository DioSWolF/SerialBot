#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from random import randrange
import aiofiles
import aiohttp
from bs4 import BeautifulSoup, element
from fake_useragent import UserAgent

from config.search_dicts import ONGOING_LIST_FIND_DICT
from config.bot_token import server_time, save_image_folder
from database.mymodels import AnimeDB, OngoingBD, session_db

from parse.find_anime import Anime
from parse.ongoing_find import AnimePageOng, EngTitleOng, ImageAnimeOng, RusTitleOng


class OngoingAnime:
    fake_agent_model = UserAgent
    ongoing_model = OngoingBD
    anime_db_model = AnimeDB
    client_session_model = aiohttp.ClientSession
    bs_soup_model = BeautifulSoup
    ong_dc_model = ONGOING_LIST_FIND_DICT
    session = session_db
    image_path = save_image_folder

    def __init__(self) -> None:
        self.date = (datetime.now() + timedelta(hours=server_time)).date()

    async def find_anime_ongoing(self) -> None:
        self.clean_table()

        page_num = 1

        async with self.client_session_model() as self.client_session:
            for search_key, site_info in self.ong_dc_model.items():
                while True:
                    self.search_key = search_key

                    for cookie_text, marker in self.ong_dc_model[self.search_key][
                        "Cookie_text"
                    ].items():
                        self.marker = marker

                        self.headers = {
                            "User-Agent": self.fake_agent_model().random,
                            "Keep-Alive": str(randrange(60, 100)),
                            "Connection": "keep-alive",
                            "Cookie": self.ong_dc_model[self.search_key]["Cookie"]
                            + cookie_text,
                        }

                        if self.search_key == "animego":
                            parse_site = (
                                site_info["link"]
                                + site_info["page_list"]
                                + str(page_num)
                            )

                        else:
                            parse_site = site_info["link"] + site_info["page_list"]

                        async with self.client_session.get(
                            parse_site, headers=self.headers
                        ) as resp:
                            if resp.status == 200:
                                self.soup = self.bs_soup_model(
                                    await resp.text(), "lxml"
                                )
                                await self._add_anime_ong()

                    if (
                        resp.status == 404
                        or site_info["stop_parse"] != ""
                        or cookie_text == site_info["stop_parse"]
                    ):
                        break

                    page_num += 1

    async def _add_anime_ong(self) -> None:
        # try:
        self.soup = self.soup.select_one(self.ong_dc_model[self.search_key]["select"])
        for el in self.soup:
            if isinstance(el, element.NavigableString):
                continue

            self._parse_anime_ong(el)

            self.anime_info = (
                self.session.query(self.anime_db_model)
                .filter_by(eng_title=self.parse_anime.eng_title)
                .first()
            )

            if self.anime_info == None:
                self._add_anime_ong_bd()
                await self._save_image()

            self._add_ong_table()
        # except:
        #     print(self.soup)

    def _add_ong_table(self) -> None:
        ong_table_anim = (
            self.session.query(self.ongoing_model)
            .filter_by(anime_id=self.anime_info.anime_id)
            .first()
        )

        if ong_table_anim == None:
            ongoing = self.ongoing_model(
                anime_id=self.anime_info.anime_id,
                date_update=self.date,
                marker=self.marker,
            )

            self.session.add(ongoing)
            self.session.commit()

    def _parse_anime_ong(self, el) -> None:
        eng_title = EngTitleOng(el, self.search_key).value
        rus_title = RusTitleOng(el, self.search_key).value
        page_anime = AnimePageOng(el, self.search_key).value
        image_anime = ImageAnimeOng(el, self.search_key)

        self.parse_anime = Anime(eng_title, rus_title, page_anime, image_anime)

    async def _get_image(self) -> None:
        resp = await self.client_session.request(
            method="GET", headers=self.headers, url=self.parse_anime.image.page
        )
        return resp

    def _add_anime_ong_bd(self) -> None:
        self.anime_info = self.anime_db_model(
            eng_title=self.parse_anime.eng_title,
            rus_title=self.parse_anime.rus_title,
            anime_page=self.parse_anime.page,
            image_page=self.parse_anime.image.page,
            image_name=self.parse_anime.image.name,
            anime_site_link=self.search_key,
        )

        self.session.add(self.anime_info)
        self.session.commit()

    async def _save_image(self) -> None:
        resp = await self._get_image()

        if resp and resp.status == 200:
            image_path = (
                self.image_path + self.search_key + "/" + self.parse_anime.image.name
            )

            async with aiofiles.open(image_path, "wb") as f:
                await f.write(await resp.read())

                self.session.query(self.anime_db_model).filter_by(
                    eng_title=self.parse_anime.eng_title
                ).update(
                    {
                        self.anime_db_model.image_name: self.parse_anime.image.name,
                        self.anime_db_model.image_path: self.image_path
                        + self.search_key
                        + "/",
                    },
                    synchronize_session=False,
                )

        self.session.commit()

    def clean_table(self):
        self.session.query(self.ongoing_model).filter(
            self.ongoing_model.date_update != self.date
        ).delete()
        self.session.commit()
