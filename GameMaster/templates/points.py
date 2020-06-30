# -*- coding: utf-8 -*-

from discord import Embed, Member, Color

from GameMaster.utils.database.basic import now
from GameMaster.utils.database.points import points_to_level


def profile_em(member: Member, points):
    level = points_to_level(points)
    level = level['level_id'] if level else 0
    return Embed(
        title=member.display_name,
        description='\u200b',
        color=Color.blue()
    ).add_field(
        name='Punkty',
        value=points
    ).add_field(
        name='Poziom',
        value=level
    ).set_thumbnail(
        url=member.avatar_url
    )


def ranking_em(ranking: str):
    return Embed(
        title=':trophy: Ranking',
        color=Color.dark_gold()
    ).add_field(
        name='\u200b',
        value=ranking
    ).set_footer(
        text=now().strftime('%Y-%m-%d %H:%M')
    )
