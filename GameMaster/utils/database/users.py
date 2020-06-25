# -*- coding: utf-8 -*-
from GameMaster.utils.database.basic import execute


def add_user(uid: int):
    return execute(
        'INSERT INTO users VALUES (%s::bigint);',
        [uid]
    )


def del_user(uid: int):
    return execute(
        'DELETE FROM users WHERE user_id = %s;',
        [uid]
    )


def check_user(uid: int):
    if not execute(
        'SELECT * FROM users WHERE user_id = %s;',
        [uid]
    ):
        add_user(uid)
