# -*- coding: utf-8 -*-
from GameMaster.utils.database.basic import execute


def get_level(user_id: int):
    points = execute(
        'SELECT points FROM users WHERE user_id = %s',
        [user_id]
    )
    if points:
        return points[0]
    else:
        return 0
