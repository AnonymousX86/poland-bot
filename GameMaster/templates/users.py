# -*- coding: utf-8 -*-
from discord import Member, Embed

from GameMaster.utils.database.points import points_to_level, get_points
from GameMaster.utils.database.warns import get_warn
from GameMaster.utils.users import translate_status


def profile_em(member: Member) -> Embed:
    points = get_points(member.id)
    level = points_to_level(points)
    level = level['level_id'] if level else 0
    return Embed(
        title=str(member),
        color=member.color
    ).add_field(
        name='Status',
        value=translate_status(str(member.status)).capitalize()
    ).add_field(
        name='Nick',
        value=member.nick or 'Brak'
    ).add_field(
        name='Punkty',
        value=points
    ).add_field(
        name='Poziom',
        value=level
    ).add_field(
        name='Ostrzeżenia',
        value=get_warn(member.id) or '0'
    ).set_thumbnail(
        url=member.avatar_url
    )
