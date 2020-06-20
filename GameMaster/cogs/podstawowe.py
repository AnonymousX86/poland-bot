# -*- coding: utf-8 -*-
from datetime import datetime as d

from discord.ext.commands import Cog, command

from GameMaster.templates.basic import info_em
from GameMaster.templates.utils import ping_em
from GameMaster.utils.datetime import utc_to_local, delta_time


class Podstawowe(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='ping',
        brief='Sprawdza opóźnienie.',
        description='Różnica jest liczona między Twoją wiadomością, a momentem kiedy bot ją odczyta.'
    )
    async def ping(self, ctx,):
        start_time = d.timestamp(utc_to_local(ctx.message.created_at))
        switch = delta_time(start_time)
        if switch < 0:
            switch = 0
        await ctx.send(embed=ping_em(switch))

    @command(
        name='role',
        description='Spis ról wraz z ID.'
    )
    async def role(self, ctx):
        roles_list = [f'{role.id} : {role}\n' for role in ctx.guild.roles]
        await ctx.send(embed=info_em(f'```\n{"".join(roles_list)}\n```'))


def setup(bot):
    bot.add_cog(Podstawowe(bot))
