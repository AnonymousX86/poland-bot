# -*- coding: utf-8 -*-
from typing import Dict

from GameMaster.utils.database.basic import execute, now


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
