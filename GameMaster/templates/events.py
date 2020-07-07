# -*- coding: utf-8 -*-
from discord import Embed, Color


def event_confirm_em(text: str) -> Embed:
    return Embed(
        title='Nowe wydarzenie',
        color=Color.orange()
    ).add_field(
        name='Opis',
        value=text
    ).add_field(
        name='Potwierdzenie',
        value='Czy zgadza się?'
    )


def new_event_em(text: str) -> Embed:
    return Embed(
        title=':dolls: Nowy event!',
        color=Color.dark_orange()
    ).add_field(
        name='Temat',
        value=text
    ).add_field(
        name='\u200b',
        value='Szczegóły zaraz zostaną podane.'
    )
