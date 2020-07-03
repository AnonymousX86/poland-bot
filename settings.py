# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from os import getenv

load_dotenv()


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
    return '1.0.0'
