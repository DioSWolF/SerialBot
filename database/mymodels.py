#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from sqlalchemy import (
    VARCHAR,
    Text,
    create_engine,
    Column,
    Integer,
    ForeignKey,
    Boolean,
    Date,
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from config.bot_token import db_folder


engine = create_engine(db_folder)
DBSession = sessionmaker(bind=engine)

session_db = DBSession()

Base = declarative_base()


class AnimeTodayDB(Base):
    __tablename__ = "anime_today_table"

    anime_id = Column(Text, primary_key=True)
    rus_name = Column(Text, nullable=True)
    eng_name = Column(Text, nullable=False)
    series_number = Column(Text, nullable=True)
    voice_acting = Column(Text, nullable=False)
    anime_page = Column(Text, nullable=False)
    update_date = Column(Date, nullable=False)
    site_name = Column(Text, nullable=False)


class PushUserDB(Base):
    __tablename__ = "push_user_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    anime_id = Column(Text, nullable=False)
    anime_name = Column(Text, nullable=False)
    push_flag = Column(Boolean, nullable=True, default=False)
    update_date = Column(Date, nullable=False)
    anime_page = Column(Text, nullable=False)
    message_text = Column(Text, nullable=False)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class UserInfoDB(Base):
    __tablename__ = "user_info_table"

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    user_login = Column(Text, nullable=True)
    user_name = Column(Text, nullable=False)
    is_bot = Column(Boolean, nullable=False)
    language_code = Column(VARCHAR(50), nullable=False)
    is_premium = Column(Text, nullable=True)
    status_subscription = Column(Boolean, default=True, nullable=False)
    update_date = Column(Date, default=datetime.now().date(), nullable=True)

    chose_site = Column(Text, nullable=True, default="anitube")

    anime_list_t = relationship(
        "AnimeDB", secondary="user_to_anime_table", back_populates="user_info_list_t"
    )

    find_anime_t = relationship(
        "AnimeDB", secondary="pagin_user_anime", back_populates="find_user_info_t"
    )


class AnimeDB(Base):
    __tablename__ = "anime_table"

    anime_id = Column(Integer, primary_key=True, autoincrement=True)
    eng_title = Column(Text, nullable=False)
    rus_title = Column(Text, nullable=True)
    anime_page = Column(Text, nullable=False)
    image_name = Column(Text, nullable=True)
    image_page = Column(Text, nullable=True)
    image_path = Column(Text, nullable=True)
    anime_site_link = Column(Text, nullable=False)

    user_info_list_t = relationship(
        "UserInfoDB", secondary="user_to_anime_table", back_populates="anime_list_t"
    )

    find_user_info_t = relationship(
        "UserInfoDB", secondary="pagin_user_anime", back_populates="find_anime_t"
    )

    anime_ongoing = relationship("OngoingBD", backref="anime_table")


class UserToAnimeDB(Base):
    __tablename__ = "user_to_anime_table"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("user_info_table.user_id"))
    anime_id = Column(Integer, ForeignKey("anime_table.anime_id"))


class FindAnimeBD(Base):
    __tablename__ = "pagin_user_anime"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_info_table.user_id"))
    anime_id = Column(Integer, ForeignKey("anime_table.anime_id"))


class OngoingBD(Base):
    __tablename__ = "ongoing_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anime_id = Column(Integer, ForeignKey("anime_table.anime_id"))
    date_update = Column(Date, nullable=False)
    marker = Column(Text, nullable=True)


class AnaliticUserBD(Base):
    __tablename__ = "analitic_user_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    new_users = Column(Integer, nullable=True, default=0)
    all_users = Column(Integer, nullable=True, default=0)
    subscript_month_users = Column(Integer, nullable=True, default=0)
    all_subscription_users = Column(Integer, nullable=True, default=0)
    all_push_users = Column(Integer, nullable=True, default=0)

    date_create = Column(
        Date,
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=1
        ).date(),
        nullable=False,
    )


class AnaliticClickBD(Base):
    __tablename__ = "analitic_click_table"

    id = Column(Integer, primary_key=True, autoincrement=True)

    start_bot = Column(Integer, nullable=True, default=0)
    month_start_bot = Column(Integer, nullable=True, default=0)

    find_anime = Column(Integer, nullable=True, default=0)
    month_find_anime = Column(Integer, nullable=True, default=0)

    new_today = Column(Integer, nullable=True, default=0)
    month_new_today = Column(Integer, nullable=True, default=0)

    change_site = Column(Integer, nullable=True, default=0)
    month_change_site = Column(Integer, nullable=True, default=0)

    show_all = Column(Integer, nullable=True, default=0)
    month_show_all = Column(Integer, nullable=True, default=0)

    date_create = Column(
        Date,
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=1
        ).date(),
        nullable=False,
    )


# Base.metadata.create_all(engine)
# Base.metadata.bind = engine
# session_db.commit()
