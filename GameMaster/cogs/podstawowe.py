# -*- coding: utf-8 -*-
from datetime import datetime as d

from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import info_em, bot_info_em, guild_info_em, rules_em, invite_em, \
    github_em, changelog_em
from GameMaster.templates.utils import ping_em
from GameMaster.utils.datetime import utc_to_local, delta_time


class Podstawowe(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='bot',
        brief='Informacje na temat bota.',
        aliases=['botinfo']
    )
    async def my_bot_info(self, ctx):
        await ctx.send(embed=bot_info_em(self.bot))

    @command(
        name='serwer',
        brief='Informacje na temat serwera.',
        aliases=['server', 'serverinfo', 'guildinfo']
    )
    async def guild_info(self, ctx):
        await ctx.send(embed=guild_info_em(ctx.guild))

    @command(
        name='ping',
        brief='Sprawdza opóźnienie.',
        description='Różnica jest liczona między czasem wysłania twojej wiadomości,'
                    ' a momentem kiedy bot ją odczyta.'
    )
    async def ping(self, ctx):
        start_time = d.timestamp(utc_to_local(ctx.message.created_at))
        switch = delta_time(start_time)
        if switch < 0:
            switch = 0
        await ctx.send(embed=ping_em(switch))

    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    @command(
        name='role',
        brief='Spis ról wraz z ID.'
    )
    async def role(self, ctx):
        roles_list = [f'{role.id} : {role}\n' for role in ctx.guild.roles]
        await ctx.send(embed=info_em(f'```\n{"".join(roles_list)}\n```'))

    @command(
        name='regulamin',
        brief='Wyświetla punkt regulaminu.',
        help='Przy braku podania punktu, wyświetlany jest kanał z regulaminem i pomoc jak używać komendy.',
        usage='[punkt]',
        aliases=['reg']
    )
    async def regulamin(self, ctx, point=None):
        try:
            point = int(point)
        except TypeError:
            point = None
        except ValueError:
            point = None
        await ctx.send(embed=rules_em(point))

    @command(
        name='zaproszenie',
        brief='Pokazuje permanentny link zaproszeniowy.',
        aliases=['invite']
    )
    async def invite(self, ctx):
        await ctx.send(embed=invite_em())

    @command(
        name='github',
        brief='Pokazuje link do kodu źródłowego bota.',
        aliases=['kod']
    )
    async def github(self, ctx):
        await ctx.send(embed=github_em())

    @command(
        name='changelog',
        brief='Zmiany bota.'
    )
    async def changelog(self, ctx):
        await ctx.send(embed=changelog_em())


def setup(bot):
    bot.add_cog(Podstawowe(bot))
