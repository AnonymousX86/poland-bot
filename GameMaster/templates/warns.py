# -*- coding: utf-8 -*-
from discord import Embed, Color


def warns_em(warns: str) -> Embed:
    return Embed(
        title=':orange_book: Lista ostrzeżeń',
        description=warns,
        color=Color.gold()
    )
