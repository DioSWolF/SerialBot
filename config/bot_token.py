#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot.async_telebot
from telebot.asyncio_storage import StateMemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler


contact_me = "DioSWolF"

bot_id = 5971988375

id_list = ()
server_time = 3

token = ""  # new token
#
save_image_folder = r"./image_list/" # path to image folder
report_path = "./report_data.xlsx" # path to report file
base_path = "" # path to database

db_folder = r"" # path to database

bot = telebot.async_telebot.AsyncTeleBot(token, state_storage=StateMemoryStorage())

scheduler = AsyncIOScheduler({"apscheduler.job_defaults.max_instances": 2})