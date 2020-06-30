# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta
from typing import Tuple, List

from psycopg2 import connect

from settings import get_db_url


def now():
    return datetime.now(timezone(timedelta(hours=1)))


def execute(query: str, args: List = None) -> Tuple[Tuple]:
    if args is None:
        args = []
    with connect(get_db_url(), sslmode='require') as conn:
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
