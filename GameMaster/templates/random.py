# -*- coding: utf-8 -*-
from discord import Embed, Color


def dice_em(result: list, sep: str = ', ') -> Embed:
    sep = f'**{sep}**'
    if len(result) == 1:
        return Embed(
            title=':game_die: Rzut kością',
            description=f'Wynik: **{result[0]}**.',
            color=Color.dark_red()
        )
    else:
        return Embed(
            title=':game_die: Rzut kośćmi',
            description=f'Wyniki: **{sep.join(result)}**.',
            color=Color.dark_red()
        )


def choose_em(emoji, thing) -> Embed:
    return Embed(
        title=f'{emoji}  {thing}',
        color=Color.blue()
    )
