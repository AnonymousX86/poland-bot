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


def eight_ball_em(answer) -> Embed:
    return Embed(
        title=f':8ball:  {answer}',
        color=Color.from_rgb(19, 22, 24)
    )


def rate_em(thing, rate) -> Embed:
    return Embed(
        title=':thumbsup: Dobre' if rate >= 5 else ':thumbsdown: Słabe',
        description=f'Oceniam **{thing}** na **{rate}/10**.',
        color=Color.orange()
    ).add_field(
        name='\u200b',
        value=':star: ' * rate
    )
