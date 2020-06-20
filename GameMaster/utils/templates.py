# -*- coding: utf-8 -*-
from discord import Embed, Color


def error_em(text, title=':red_circle: Błąd!', color=Color.red()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def success_em(text, title=':green_circle: Gotowe!', color=Color.green()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def please_wait_em(text='', title=':hourglass_flowing_sand: Daj mi chwilę...', color=Color.gold()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def info_em(text='', title=':information_source: Informacja', color=Color.blue()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def dice_em(result: list, sep: str = ', ') -> Embed:
    if len(result) < 8:
        return Embed(
            title=f':game_die: {sep.join(result)}',
            color=Color.dark_red()
        )
    else:
        return Embed(
            title=':game_die:',
            description=sep.join(result),
            color=Color.dark_red()
        )