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
    if len(result) == 1:
        return Embed(
            title=':game_die: Rzut kością',
            description= f'Wyrzucono `{sep.join(result)}',
            color=Color.dark_red()
        )
    else:
        return Embed(
            title=':game_die: Rzut kośćmi',
            description=f'Wyrzucone wartości: `{sep.join(result}`',
            color=Color.dark_red()
        )
                                                
def ping(p) -> Embed:
    kolor;
    
    if p < 300:
        kolor = Color.green();   
    elif p >= 300 and p < 1000:
        kolor = Color.orange();
    else:
        kolor = Color.red();
    
    return Embed(
        title=':ping_pong: Pong',
        description=f'Ping bota wynosi {p} ms',
        color=kolor
    )
