# -*- coding: utf-8 -*-
from typing import Dict, List

from GameMaster.utils.database.basic import execute
from GameMaster.utils.database.users import check_user


def points_to_level(points: int) -> Dict:
    level = execute(
        'SELECT level_id, min_points, max_points, role_id '
        'FROM levels '
        'WHERE (( '
        '   ( %s >= min_points ) '
        '       AND '
        '   ( %s <= max_points ) '
        '));',
        [points, points]
    )
    return {
        'level_id': level[0][0],
        'min_points': level[0][1],
        'max_points': level[0][2],
        'role_id': level[0][3]
    } if level else {}


def get_points(uid: int) -> int:
    points = execute(
        'SELECT points FROM users WHERE user_id = %s',
        [uid]
    )
    return points[0][0] if points else 0


def get_all_points(limit=10) -> List:
    points = execute(
        'SELECT user_id, points FROM users LIMIT %s;',
        [limit]
    )
    return [[item[0], item[1]] for item in points] if points else []


def manage_points(uid: int, points: int):
    check_user(uid)
    base = execute(
        'SELECT points FROM users WHERE user_id = %s;',
        [uid]
    )[0][0] or 0
    points += base
    execute(
        'UPDATE users SET points = %s WHERE user_id = %s;',
        [points, uid]
    )


def add_points(uid: int, points: int):
    manage_points(uid, points)


def remove_points(uid: int, points: int):
    manage_points(uid, -points)
