# -*- coding: utf-8 -*-
from typing import Tuple, Dict

from GameMaster.utils.database.basic import execute, now
from GameMaster.utils.database.users import check_user


def get_warn(uid: int) -> Tuple[Tuple]:
    return execute('SELECT * FROM warns WHERE user_id = %s;', [uid])


def get_warns() -> Dict:
    records = execute('SELECT warn_id, user_id, warn_level, warn_date, warn_time, warn_reason FROM warns;')
    result = {}
    if records:
        for r in records:
            result[r[0]] = {
                'warn_id': r[0],
                'user_id': r[1],
                'warn_level': r[2],
                'warn_date': r[3],
                'warn_time': r[4],
                'warn_reason': r[5]
            }
    else:
        result = {{}}
    return result


def add_warn(uid: int, reason=None, level=None):
    today = now()
    warn_level = get_warn(uid)
    if level is None:
        level = warn_level[0][1] if warn_level else 1
    check_user(uid)
    return execute(
        'INSERT INTO warns'
        ' (user_id, warn_level, warn_date, warn_time, warn_reason)'
        ' VALUES (%s::bigint, %s, %s, %s, %s);',
        [uid, level, today.strftime('%Y-%m-%d'), today.strftime('%H:%M:%S'), reason]
    )


def update_warn(uid: int, reason=None):
    today = now()
    return execute(
        'UPDATE warns'
        ' SET warn_date = %s, warn_time = %s, warn_reason = %s'
        ' WHERE user_id = %s;',
        [today.strftime('%Y-%m-%d'), today.strftime('%H:%M:%S'), reason, uid]
    )


def del_warns(uid: int):
    return execute(
        'DELETE FROM warns WHERE user_id = %s;',
        [uid]
    )


if __name__ == '__main__':
    q = get_warns()
    breakpoint()
