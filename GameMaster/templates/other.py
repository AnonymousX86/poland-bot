# -*- coding: utf-8 -*-
from discord import Embed, Color, Member

from GameMaster.utils.users import translate_status


def member_em(member: Member) -> Embed:
    return Embed(
        title=str(member),
        color=member.color
    ).add_field(
        name='Status',
        value=translate_status(str(member.status)).capitalize()
    ).add_field(
        name='Nick',
        value=member.nick or 'Brak'
    ).set_thumbnail(
        url=member.avatar_url
    )


def warns_em(warns: str) -> Embed:
    return Embed(
        title=':orange_book: Lista ostrzeżeń',
        description=warns,
        color=Color.gold()
    )
