# -*- coding: utf-8 -*-
from random import randint

from discord import HTTPException
from discord.ext.commands import Cog, command

from GameMaster.utils.templates import error_em, dice_em


class Ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='ping',
        brief='Pokazuje ping bota',
        aliases=['pong']
    )
    async def ping(self, ctx):
          await ctx.send(embed=ping(bot.latency))


def setup(bot):
    bot.add_cog(Losowe(bot))
