# -*- coding: utf-8 -*-
from os import getenv
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

_bot_version = '1.1.0'


def warn_roles_ids() -> Dict:
    return {
        1: 713401249797505135,
        2: 713401427929858069,
        3: 713401508292591777
    }


def get_bot_token() -> str:
    return getenv('BOT_TOKEN')


def get_db_url() -> str:
    return getenv('DATABASE_URL')


def bot_version() -> str:
    return _bot_version
