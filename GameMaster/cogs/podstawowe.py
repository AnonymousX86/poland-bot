# -*- coding: utf-8 -*-
from datetime import datetime as d

from discord import HTTPException, NotFound
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import info_em, error_em, success_em, bot_info_em, guild_info_em
from GameMaster.templates.utils import ping_em
from GameMaster.utils.datetime import utc_to_local, delta_time
from GameMaster.utils.users import check_mention


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
        aliases=['serverinfo', 'guildinfo']
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

    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(
        name='kick',
        brief='Wyrzuca z serwera.',
        usage='<użytkownik>'
    )
    async def kick(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo wyrzucić.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                member = ctx.guild.get_member(user_id)
                if not member:
                    await ctx.send(embed=error_em('Ten użytkownik nie znajduje się na serwerze.'))
                else:
                    try:
                        await member.kick(reason=f'Wyrzucony przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas wyrzucania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie wyrzucono **{member}**.'))

    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(
        name='ban',
        brief='Banuje z serwera.',
        usage='<użytkownik>'
    )
    async def ban(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo zbanować.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                member = ctx.guild.get_member(user_id)
                if not member:
                    await ctx.send(embed=error_em('Ten użytkownik nie znajduje się na serwerze.'))
                else:
                    try:
                        await member.ban(reason=f'Zbanowany przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas banowania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie zbanowano **{member}**.'))

    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(
        name='unban',
        brief='Usuwa ban z serwera.',
        usage='<użytkownik>'
    )
    async def unban(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo odbanować.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                try:
                    user = await self.bot.fetch_user(user_id)
                except NotFound:
                    await ctx.send(embed=error_em('Ten użytkownik nie istnieje.'))
                else:
                    try:
                        await user.unban(reason=f'Odbanowany przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas odbanowania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie odbanowano **{user}**.'))


def setup(bot):
    bot.add_cog(Podstawowe(bot))
