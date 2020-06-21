# -*- coding: utf-8 -*-
from discord.ext.commands import Cog, command


class Poziomy(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='punkty'
    )
    async def punkty(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Poziomy(bot))
