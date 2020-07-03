# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def get_bot_token() -> str:
    return getenv('BOT_TOKEN')


def get_db_url() -> str:
    return getenv('DATABASE_URL')


def bot_version() -> str:
    return '1.0.0'
