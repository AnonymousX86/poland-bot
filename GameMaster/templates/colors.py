# -*- coding: utf-8 -*-
from discord import Embed, Color


def color_em(color: str) -> Embed:
    return Embed(
        title=color.upper(),
        description='\u200b',
        color=Color.dark_grey()
    ).set_thumbnail(
        url='https://dummyimage.com/256/{0}/{0}.png'.format(color[1::])
    )
