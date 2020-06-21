# -*- coding: utf-8 -*-
from typing import Tuple

from GameMaster.utils.database.basic import execute, now


def get_warn(uid: int) -> Tuple[Tuple]:
    return execute('SELECT * FROM warns WHERE uid = %s;', [uid])


def get_warns() -> Tuple[Tuple]:
    return execute('SELECT * FROM warns;')


def set_warn(uid: int, reason='brak', level=1):
    today = now()
    return execute(
        'INSERT INTO warns VALUES (%s::bigint, %s, %s, %s, %s);',
        [uid, level, today.strftime('%Y-%m-%d'), today.strftime('%H:%M:%S'), reason]
    )


def add_warn(uid: int, reason=None, level=None):
    today = now()
    if level is None:
        level = get_warn(uid)[0][1] + 1
    return execute(
        'UPDATE warns SET level = %s, date = %s, time = %s, reason = %s WHERE uid = %s;',
        [level, today.strftime('%Y-%m-%d'), today.strftime('%H:%M:%S'), reason, uid]
    )


def update_warn(uid: int, reason=None):
    today = now()
    return execute(
        'UPDATE warns SET date = %s, time = %s, reason = %s WHERE uid = %s;',
        [today.strftime('%Y-%m-%d'), today.strftime('%H:%M:%S'), reason, uid]
    )


def del_warns(uid: int):
    return execute(
        'DELETE FROM warns WHERE uid = %s;',
        [uid]
    )
