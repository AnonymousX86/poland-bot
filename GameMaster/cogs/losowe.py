# -*- coding: utf-8 -*-
from random import randint

from discord import HTTPException
from discord.ext.commands import Cog, command

from GameMaster.utils.templates import error_em, dice_em


class Losowe(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='kostka',
        brief='Rzuca kością.',
        description='Może rzucić różną ilością kości o różnych ilościach ścianek.',
        help='Ściany kostki muszą być co najmniej cztery, a rzut przynajmniej jeden.'
             ' Domyślnymi wartościami są: 6 (ściany) i 1 (rzut).'
             ' Dodatkowo można dodać własny separator (domyślnie ", ").',
        aliases=['kość', 'k'],
        usage='[ściany] [rzuty] [separator]'
    )
    async def kostka(self, ctx, k=6, x=1, sep=', '):
        try:
            k = int(k)
            x = int(x)
        except ValueError:
            await ctx.send(embed=error_em('Co najmniej jednej błędny argument.'))
        else:
            if k < 4 or x < 1:
                await ctx.send(embed=error_em('Co najmniej jednej błędny argument.'))
            else:
                result = []
                for i in range(x):
                    result.append(str(randint(1, k)))
                try:
                    await ctx.send(embed=dice_em(result, sep))
                except HTTPException:
                    await ctx.send(embed=error_em('Zbyt duże wartości!'))


def setup(bot):
    bot.add_cog(Losowe(bot))
