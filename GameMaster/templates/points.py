# -*- coding: utf-8 -*-

from discord import Embed, Color

from GameMaster.utils.database.basic import now


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
