#!/usr/bin/env python
# -*- coding: utf-8 -*-


from abc import ABC, abstractclassmethod
import uuid

from bs4 import BeautifulSoup


class ValueOngoing(ABC):
    def __init__(self, value, search_key) -> None:
        self.search_key = search_key
        self.__value: str = ""
        self.value: str = value

    @property
    @abstractclassmethod
    def value(self) -> str:
        pass

    @value.setter
    @abstractclassmethod
    def value(self, value) -> str:
        pass


class EngTitleOng(ValueOngoing):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        if self.search_key == "animego":
            value = value.select_one(".text-gray-dark-6").text

        if self.search_key == "anitube":
            value = value.select_one(".text_content a").text

        if self.search_key == "hdrezka":
            value = value.select_one(".b-content__inline_item-link a").text

        self.__value = value


class RusTitleOng(ValueOngoing):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        if self.search_key == "animego":
            value = value.select_one(".h5 a").text

        if self.search_key == "anitube":
            value = value.select_one(".text_content a").text

        if self.search_key == "hdrezka":
            value = value.select_one(".b-content__inline_item-link a").text

        self.__value = value


class AnimePageOng(ValueOngoing):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> str:
        if self.search_key == "animego":
            value = value.select_one(".h5 a").get("href")

        if self.search_key == "anitube":
            value = value.select_one(".text_content a").get("href")

        if self.search_key == "hdrezka":
            value = "https://rezka.ag/" + value.select_one(
                ".b-content__inline_item-link a"
            ).get("href")

        self.__value = value


class ImageAnimeOng:
    def __init__(self, image_name: BeautifulSoup, search_key: str) -> None:
        self.search_key = search_key
        self.__name: str = ""
        self.name: str = image_name
        self.__page: str = ""
        self.page: str = image_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name) -> str:
        name = f"{uuid.uuid4()}.jpg"
        self.__name = name

    @property
    def page(self) -> str:
        return self.__page

    @page.setter
    def page(self, page) -> str:
        if self.search_key == "animego":
            page = page.select_one(".anime-list-lazy").get("data-original")

        if self.search_key == "anitube":
            page = page.select_one(".sl_poster img").get("src")
            page = "https://anitube.in.ua" + page

        if self.search_key == "hdrezka":
            page = page.select_one(".b-content__inline_item-cover img").get("src")

        self.__page = page
