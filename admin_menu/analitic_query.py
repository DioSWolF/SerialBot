#!/usr/bin/env python
# -*- coding: utf-8 -*-


import aiofiles
from database.mymodels import (
    AnaliticClickBD,
    AnaliticUserBD,
    AnimeDB,
    AnimeTodayDB,
    FindAnimeBD,
    PushUserDB,
    UserToAnimeDB,
    session_db,
)
from telebot.types import CallbackQuery
import pandas
from config.bot_token import report_path


class AdminCleanTable:

    """
    The AdminCleanTable class provides functionality to delete data from the database.

    :param session: The database session
    :type session: sqlalchemy.orm.session.Session

    :param anime_model: The model for anime
    :type anime_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param anime_today_model: AThe model for anime list today
    :type anime_today_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param find_anime_model: The model for  find anime list
    :type find_anime_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param user_anime_model: The model for user anime list
    :type user_anime_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param user_push_model: The model for user push
    :type user_push_model: sqlalchemy.ext.declarative.api.DeclarativeMeta
    """

    session = session_db

    anime_model = AnimeDB
    anime_today_model = AnimeTodayDB
    find_anime_model = FindAnimeBD
    user_anime_model = UserToAnimeDB
    user_push_model = PushUserDB

    def clean_anime_today(self, *args) -> None:
        """
        Delete all data from AnimeTodayDB model.

        :param args: all
        :return: None
        :rtype: None
        """

        self.session.query(self.anime_today_model).delete()
        self.session.commit()

    def clean_anime(self, *args) -> None:
        """
        Delete all data from PushUserDB model.

        :param args: all
        :return: None
        :rtype: None
        """

        self.session.query(self.anime_model).delete()
        self.session.commit()

    def clean_user_push(self, *args) -> None:
        """
        Delete all data from PushUserDB model.

        :param args: all
        :return: None
        :rtype: None
        """

        self.session.query(self.user_push_model).delete()
        self.session.commit()

    def clean_find_anime(self, *args) -> None:
        """
        Delete all data from FindAnimeBD model.

        :param args: all
        :return: None
        :rtype: None
        """

        self.session.query(self.find_anime_model).delete()
        self.session.commit()

    def clean_all_table(self, *args) -> None:
        """
        Delete all data from all models.

        :param args: all
        :return: None
        :rtype: None
        """

        self.clean_anime_today()
        self.clean_user_push()
        self.clean_find_anime()
        self.clean_anime()


class AnaliticInfo:

    """
    A class for generating reports from analytical data.

    :param session: Session object
    :type session: sqlalchemy.orm.session.Session

    :param click_model: The model for analitic user clickers
    :type click_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param user_model: The model for user analitic
    :type user_model: sqlalchemy.ext.declarative.api.DeclarativeMeta

    :param xlsx_path: The path to the report to be generated.
    :type xlsx_path: str

    :param dataframe_model: Pandas DataFrame model
    :type dataframe_model: pandas.DataFrame
    """

    session = session_db
    click_model = AnaliticClickBD
    user_model = AnaliticUserBD
    xlsx_path = report_path
    dataframe_model = pandas.DataFrame

    def get_all_click(self) -> None:
        """
        Get all clicks from the database.

        :return: None
        :rtype: None
        """

        self.all_click: list[AnaliticClickBD] = self.session.query(
            self.click_model
        ).all()

    def get_all_user(self) -> None:
        """
        Get all users from the database.

        :return: None
        :rtype: None
        """

        self.all_user: list[AnaliticUserBD] = self.session.query(self.user_model).all()

    def get_all(self) -> None:
        """
        Get all clicks and users from the database.

        :return: None
        :rtype: None
        """

        self.get_all_click()
        self.get_all_user()

    def get_all_date(self) -> None:
        """
        Get all dates from the database.

        :return: None
        :rtype: None
        """

        all_date = self.session.query(self.click_model.date_create).all()
        self.all_date = [date[0] for date in all_date]

    def _get_month_click(self) -> None:
        """
        Get click data for a specific month.

        :return: None
        :rtype: None
        """

        self.month_click: AnaliticClickBD = (
            self.session.query(self.click_model)
            .filter_by(date_create=self.calldata)
            .first()
        )

    def _get_month_user(self) -> None:
        """
        Get user data for a specific month.

        :return: None
        :rtype: None
        """

        self.month_user: AnaliticUserBD = (
            self.session.query(self.user_model)
            .filter_by(date_create=self.calldata)
            .first()
        )

    def _parse_date(self, call: CallbackQuery) -> None:
        """
        Parse the date from a Telegram callback query.

        :param call: CallbackQuery

        :return: None
        :rtype: None
        """

        self.calldata = call.data.split("|||")[1]

    def get_month_all(self, date: CallbackQuery):
        """
        Get all click and user data for a specific month and generate a report.

        :param date: CallbackQuery
        :return: None
        :rtype: None
        """

        self._parse_date(date)
        self._get_month_click()
        self._get_month_user()
        self.create_report_text()

    def create_report_text(self) -> str:
        """
        Create the text for the report.

        :return: None
        :rtype: None
        """

        self.report_text = f"User statistic date:    {self.month_user.date_create},\n\
        New users: {self.month_user.new_users},\n\
        All users: {self.month_user.all_users},\n\
        Subscription users: {self.month_user.all_subscription_users},\n\
        Subscription users month: {self.month_user.subscript_month_users},\n\
        Push users: {self.month_user.all_push_users}.\n\n\
Click statistic date:       {self.month_click.date_create}, \n\
        Click 'start': {self.month_click.start_bot},\n\
        Click month 'start': {self.month_click.month_start_bot},\n\
        Click 'find anime': {self.month_click.find_anime},\n\
        Click month 'find anime': {self.month_click.month_find_anime},\n\
        Click 'new today': {self.month_click.new_today},\n\
        Click month 'new today': {self.month_click.month_new_today},\n\
        Click 'change site': {self.month_click.change_site},\n\
        Click month 'change site': {self.month_click.month_change_site},\n\
        Click 'show all': {self.month_click.show_all},\n\
        Click month 'show all': {self.month_click.month_show_all}."

    def create_click_list(self) -> None:
        """
        Create a list of click data for the report.

        :return: None
        :rtype: None
        """

        self.click_rep_list = [
            [
                "Date create",
                "Click 'start'",
                "Click month 'start'",
                "Click 'find anime'",
                "Click month 'find anime'",
                "Click 'new today'",
                "Click month 'new today'",
                "Click 'change site'",
                "Click month 'change site'",
                "Click 'show all'",
                "Click month 'show all'",
            ]
        ]

        for click in self.all_click:
            click_rep = [
                str(click.date_create),
                click.start_bot,
                click.month_start_bot,
                click.find_anime,
                click.month_find_anime,
                click.new_today,
                click.month_new_today,
                click.change_site,
                click.month_change_site,
                click.show_all,
                click.month_show_all,
            ]

            self.click_rep_list.append(click_rep)

    def create_user_list(self) -> None:
        """
        Create a list of user data for the report.

        :return: None
        :rtype: None
        """

        self.user_rep_list = [
            [
                "Date create",
                "New users",
                "All users",
                "Push users (chose any film)",
                "Subscription users ta month",
                "Subscription users (all)",
            ]
        ]

        for user in self.all_user:
            user_rep_list = [
                str(user.date_create),
                user.new_users,
                user.all_users,
                user.all_push_users,
                user.subscript_month_users,
                user.all_subscription_users,
            ]

            self.user_rep_list.append(user_rep_list)

    def create_dataframe(self) -> None:
        """
        Create the pandas DataFrame for the report.

        :return: None
        :rtype: None
        """

        self.dataframe = self.dataframe_model(
            [*self.user_rep_list, *self.click_rep_list]
        )

    def write_xmlx(self) -> None:
        """
        Write the report to an Excel file.

        :return: None
        :rtype: None
        """

        with pandas.ExcelWriter(self.xlsx_path, engine="openpyxl", mode="w") as writer:
            self.dataframe.to_excel(writer)

    async def read_file(self) -> None:
        """
        Read the Excel file and return its contents as a string.

        :return: None
        :rtype: None
        """

        async with aiofiles.open(report_path, "rb") as file:
            self.file = await file.read()

    async def create_report_xmlx(self) -> None:
        """
        Create the report and save it to an Excel file.

        :return: None
        :rtype: None
        """

        self.get_all()
        self.create_click_list()
        self.create_user_list()
        self.create_dataframe()
        self.write_xmlx()
        await self.read_file()
