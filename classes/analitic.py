#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta

from typing import Any

from sqlalchemy import and_
from dateutil.relativedelta import relativedelta
from database.mymodels import (
    AnaliticClickBD,
    AnaliticUserBD,
    UserInfoDB,
    UserToAnimeDB,
    session_db,
)

from telebot.types import CallbackQuery


class AnaliticUserData:

    """
    A class that provides user analysis data.

    :param session: The database session
    :type session: sqlalchemy.orm.session.Session

    :param user_db_model: The model for user info
    :type user_db_model: UserInfoDB

    :param analitic_user_model: The model for user analytics
    :type analitic_user_model: AnaliticUserBD

    :param user_anime_model: The model for user anime preferences
    :type user_anime_model: UserToAnimeDB
    """

    session = session_db
    user_db_model = UserInfoDB
    analitic_user_model = AnaliticUserBD
    user_anime_model = UserToAnimeDB

    def __init__(self) -> None:
        """
        Initializes instance variables date_now and date_create.

        :return: None
        :rtype: None
        """
        self.date_now = datetime.now().date()
        self.date_create = datetime(
            year=self.date_now.year, month=self.date_now.month, day=1
        ).date()

    def create_data(self) -> None:
        """
        Create a new record for the current month in the database if one does not exist.

        :return: None
        :rtype: None
        """

        data = (
            self.session.query(self.analitic_user_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        if data == None:
            new_data = self.analitic_user_model()

            self.session.add(new_data)
            self.session.commit()

    def get_all_users(self) -> None:
        """
        Get all users from the database.

        :return: None
        :rtype: None
        """

        self.all_users = self.session.query(self.user_db_model).all()
        self.len_all_users = len(self.all_users)

    def get_subscription_month(self, month: int = 1) -> None:
        """
        Get all users who subscribed within the past `month` months.

        :param month: The number of months to look back. Default is 1.
        :type month: int

        :return: None
        :rtype: None
        """

        year = self.date_now.year
        month = (self.date_now.month - month) % 12 or 12

        if month > self.date_now.month:
            year -= 1

        last_month = datetime(year=year, month=month, day=1).date()
        day = (last_month + relativedelta(months=1) - timedelta(days=1)).day
        first_month = datetime(
            year=self.date_now.year, month=last_month.month, day=day
        ).date()

        self.subscript_month_users = (
            self.session.query(self.user_db_model)
            .filter(
                self.user_db_model.status_subscription == True,
                and_(
                    self.user_db_model.update_date >= last_month,
                    self.user_db_model.update_date <= first_month,
                ),
            )
            .all()
        )
        self.len_subscrip_month_users = len(self.subscript_month_users)

    def get_all_subscpirt(self) -> None:
        """
        Get all users who have subscribed.

        :return: None
        :rtype: None
        """

        self.all_subscription_users = (
            self.session.query(self.user_db_model)
            .filter_by(status_subscription=True)
            .all()
        )
        self.len_all_subscript = len(self.all_subscription_users)

    def get_all_user_from(self, date: int) -> None:
        """
        Get all users who have updated their account in the past `date` days.

        :param date: The number of days to look back.
        :type date: int

        :return: None
        :rtype: None
        """

        first_day = self.date_now - timedelta(days=date)
        self.all_users_from = (
            self.session.query(self.user_db_model)
            .filter(self.user_db_model.update_date >= first_day)
            .all()
        )
        self.len_all_users_from = len(self.all_users_from)

    def get_all_user_month(self, month: int = 0) -> None:
        """
        Get all users that have updated their subscription within the specified month.

        :param month: The number of months to look back. Default is 0.
        :type month: int

        :return: None
        :rtype: None
        """

        year = self.date_now.year
        month = (self.date_now.month - month) % 12 or 12

        if month > self.date_now.month:
            year -= 1

        last_month = datetime(year=year, month=month, day=1).date()
        day = (last_month + relativedelta(months=1) - timedelta(days=1)).day
        first_month = datetime(
            year=self.date_now.year, month=last_month.month, day=day
        ).date()

        self.all_users_month = (
            self.session.query(self.user_db_model)
            .filter(
                and_(
                    self.user_db_model.update_date >= last_month,
                    self.user_db_model.update_date <= first_month,
                )
            )
            .all()
        )
        self.len_all_users_month = len(self.all_users_month)

    def get_push_user(self) -> None:
        """
        Get all users who have selected their favorite anime.

        :return: None
        :rtype: None
        """

        self.push_user = (
            self.session.query(self.user_anime_model)
            .group_by(self.user_anime_model.user_id)
            .all()
        )
        self.len_push_user = len(self.push_user)

    def get_all(self) -> None:
        """
        Get all the data needed for analysis.

        :return: None
        :rtype: None
        """

        self.get_all_users()
        self.get_all_subscpirt()
        self.get_subscription_month()
        self.get_all_user_month()
        self.get_push_user()

    def update_new_users_month(self) -> None:
        """
        Updates the count of new users from the specified month.

        :return: None
        :rtype: None
        """

        self.session.query(self.analitic_user_model).filter_by(
            date_create=self.date_create
        ).update({self.analitic_user_model.new_users: self.len_all_users_month})

        self.session.commit()

    def update_all_subscript(self) -> None:
        """
        Updates the count of all subscribers.

        :return: None
        :rtype: None
        """

        self.session.query(self.analitic_user_model).filter_by(
            date_create=self.date_create
        ).update({self.analitic_user_model.all_subscription_users: self.len_all_users})

        self.session.commit()

    def update_subscription_month(self) -> None:
        """
        Updates the count of subscribers from the specified month.

        :return: None
        :rtype: None
        """

        self.session.query(self.analitic_user_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_user_model.subscript_month_users: self.len_subscrip_month_users
            }
        )

        self.session.commit()

    def update_all_users(self) -> None:
        """
        Updates the count of all users.

        :return: None
        :rtype: None
        """

        self.session.query(self.analitic_user_model).filter_by(
            date_create=self.date_create
        ).update({self.analitic_user_model.all_users: self.len_all_users})

        self.session.commit()

    def update_push_users(self) -> None:
        """
        Updates the number of users who have enabled push notifications.

        :return: None
        :rtype: None
        """

        self.session.query(self.analitic_user_model).filter_by(
            date_create=self.date_create
        ).update({self.analitic_user_model.all_push_users: self.len_push_user})

        self.session.commit()

    def update_all(self) -> None:
        """
        Updates all user analytics.

        :return: None
        :rtype: None
        """

        self.update_all_users()
        self.update_all_subscript()
        self.update_subscription_month()
        self.update_new_users_month()
        self.update_push_users()

    def create_month_data(self) -> None:
        """
        Creates data for the current month, and updates all user analytics.

        :return: None
        :rtype: None
        """

        self.create_data()
        self.get_all()
        self.update_all()


class AnaliticClickData:

    """
    A decorator to collect and store click data for different features of a bot

    :param session: The database session
    :type session: sqlalchemy.orm.session.Session

    :param analitic_click_model:
    :type analitic_click_model: AnaliticClickBD
    """

    session = session_db
    analitic_click_model = AnaliticClickBD

    def __init__(self, func: Any) -> None:
        """
        Initialize the decorator instance.

        :param func: The function to be decorated

        :return: None
        :rtype: None
        """

        self.func = func
        self.date_now = datetime.now().date()
        self.date_create = datetime(
            year=self.date_now.year, month=self.date_now.month, day=1
        ).date()

    async def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Store click data and call the decorated function

        :return: None
        :rtype: None
        """

        self.add_analitic(*args)

        await self.func(*args, **kwargs)

    def create_data(self) -> None:
        """
        Create new click data for the current month if it doesn't already exist.

        :return: None
        :rtype: None
        """

        data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        if data == None:
            new_data = self.analitic_click_model()
            self.session.add(new_data)
            self.session.commit()

    def create_old_date(self, month: int = 1) -> None:
        """
        Create a datetime instance for the date `month` months ago.

        :param month: The number of months to go back in time. Default is 1.
        :type month: int

        :return: None
        :rtype: None
        """

        year = self.date_now.year
        month = (self.date_now.month - month) % 12 or 12

        if month > self.date_now.month:
            year -= 1

        self.last_month = datetime(year=year, month=month, day=1).date()

    def add_start_bot(self) -> None:
        """
        Add data for the start_bot feature

        :return: None
        :rtype: None
        """

        old_click = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.last_month)
            .first()
        )

        if old_click != None:
            self.session.query(self.analitic_click_model).filter_by(
                date_create=self.date_create
            ).update({self.analitic_click_model.start_bot: old_click.start_bot})

            self.session.commit()

    def add_find_anime(self) -> None:
        """
        Add data for the find_anime feature

        :return: None
        :rtype: None
        """

        old_click = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.last_month)
            .first()
        )

        if old_click != None:
            self.session.query(self.analitic_click_model).filter_by(
                date_create=self.date_create
            ).update({self.analitic_click_model.find_anime: old_click.find_anime})

            self.session.commit()

    def add_new_today(self) -> None:
        """
        Add data for the new_today feature

        :return: None
        :rtype: None
        """

        old_click = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.last_month)
            .first()
        )

        if old_click != None:
            self.session.query(self.analitic_click_model).filter_by(
                date_create=self.date_create
            ).update({self.analitic_click_model.new_today: old_click.new_today})

            self.session.commit()

    def add_change_site(self) -> None:
        """
        Add data for the change_site feature

        :return: None
        :rtype: None
        """

        old_click = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.last_month)
            .first()
        )

        if old_click != None:
            self.session.query(self.analitic_click_model).filter_by(
                date_create=self.date_create
            ).update({self.analitic_click_model.change_site: old_click.change_site})

            self.session.commit()

    def add_show_all(self) -> None:
        """
        Add data for the show_all feature

        :return: None
        :rtype: None
        """

        old_click = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.last_month)
            .first()
        )

        if old_click != None:
            self.session.query(self.analitic_click_model).filter_by(
                date_create=self.date_create
            ).update({self.analitic_click_model.show_all: old_click.show_all})

            self.session.commit()

    def add_old_data(self) -> None:
        self.create_old_date()
        self.create_data()

        self.add_start_bot()
        self.add_find_anime()
        self.add_new_today()
        self.add_change_site()
        self.add_show_all()

    def update_start_bot(self) -> None:
        click_data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        self.session.query(self.analitic_click_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_click_model.month_start_bot: click_data.month_start_bot
                + 1,
                self.analitic_click_model.start_bot: click_data.start_bot + 1,
            }
        )

        self.session.commit()

    def update_find_anime(self) -> None:
        click_data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        self.session.query(self.analitic_click_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_click_model.month_find_anime: click_data.month_find_anime
                + 1,
                self.analitic_click_model.find_anime: click_data.find_anime + 1,
            }
        )

        self.session.commit()

    def update_new_today(self) -> None:
        click_data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        self.session.query(self.analitic_click_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_click_model.month_new_today: click_data.month_new_today
                + 1,
                self.analitic_click_model.new_today: click_data.new_today + 1,
            }
        )

        self.session.commit()

    def update_change_site(self) -> None:
        click_data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        self.session.query(self.analitic_click_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_click_model.month_change_site: click_data.month_change_site
                + 1,
                self.analitic_click_model.change_site: click_data.change_site + 1,
            }
        )

        self.session.commit()

    def update_show_all(self) -> None:
        click_data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        self.session.query(self.analitic_click_model).filter_by(
            date_create=self.date_create
        ).update(
            {
                self.analitic_click_model.month_show_all: click_data.month_show_all + 1,
                self.analitic_click_model.show_all: click_data.show_all + 1,
            }
        )

        self.session.commit()

    def update_command(self, call: CallbackQuery) -> None:
        UPDATE_DICT = {
            "/start": self.update_start_bot,
            "find_anime": self.update_find_anime,
            "find_new_series": self.update_new_today,
            "change_search_site": self.update_change_site,
            "show_all": self.update_show_all,
        }

        try:
            func = UPDATE_DICT.get(call.data.split("#")[0], self.close)

        except AttributeError:
            func = UPDATE_DICT.get(call.text, self.close)

        func()

    def add_analitic(self, call: CallbackQuery) -> None:
        data = (
            self.session.query(self.analitic_click_model)
            .filter_by(date_create=self.date_create)
            .first()
        )

        if data == None:
            self.add_old_data()

        self.update_command(call)

    def close(*_) -> None:
        pass
