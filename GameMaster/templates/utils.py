# -*- coding: utf-8 -*-
from discord import Embed, Color


def ping_em(p: int) -> Embed:
    if p > 600:
        color = Color.red()
    elif p > 200:
        color = Color.orange()
    else:
        color = Color.green()

    return Embed(
        title=':ping_pong: Pong',
        description=f'Ping wynosi **{p}** ms.',
        color=color
    )
