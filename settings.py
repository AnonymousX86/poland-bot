# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def bot_token() -> str:
    return getenv('BOT_TOKEN')


def db_url() -> str:
    return getenv('DATABASE_URL')
