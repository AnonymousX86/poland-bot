# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict

from psycopg2 import connect

from settings import db_url


def now():
    return datetime.now(timezone(timedelta(hours=1)))


def execute(query: str, args=None) -> Tuple[Tuple]:
    if args is None:
        args = []
    with connect(db_url(), sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        if query.startswith('SELECT'):
            result: tuple = cur.fetchall()
        else:
            result = (())
        conn.commit()
        cur.close()
    return result


def check_connection() -> bool:
    return True if execute('SELECT 1;') else False


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


def purge_enabled(guild_id: int) -> bool:
    q = execute('SELECT purge_enabled FROM purges WHERE guild_id = %s;', [guild_id])
    return q[0][0] if q else False


def purge_enable(guild_id: int):
    today = now()
    return execute(
        'UPDATE purges SET purge_enabled = true, purge_started_date = %s WHERE guild_id = %s;',
        [today.strftime('%Y-%m-%d'), guild_id]
    )


def purge_disable(guild_id: int):
    return execute(
        'UPDATE purges SET purge_enabled = false WHERE guild_id = %s;',
        [guild_id]
    )


def purge_settings(guild_id: int) -> Dict:
    q = execute(
        '''SELECT
            check_channel_id,
            active_role_id,
            inactive_role_id,
            purge_started_date
        FROM purges
        WHERE guild_id = %s;''',
        [guild_id]
    )[0]
    return dict(
        check_channel_id=q[0],
        active_role_id=q[1],
        inactive_role_id=q[2],
        purge_started_date=q[3]
    )
