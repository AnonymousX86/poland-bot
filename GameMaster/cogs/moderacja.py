# -*- coding: utf-8 -*-
from discord import HTTPException, NotFound, Message, TextChannel
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import error_em, success_em
from GameMaster.templates.moderate import log_message_del_em, log_message_edit_em
from GameMaster.utils.users import check_mention
from settings import get_channel_id


class Moderacja(Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @kick.error
    async def kick_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

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

    @ban.error
    async def ban_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

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

    @unban.error
    async def unban_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    @Cog.listener(
        name='on_message_delete'
    )
    async def message_delete_watch(self, message: Message):
        log_channel: TextChannel = message.guild.get_channel()
        if log_channel:
            await log_channel.send(embed=log_message_del_em(message))

    @Cog.listener(
        name='on_message_edit'
    )
    async def message_edit_watch(self, before: Message, after: Message):
        log_channel: TextChannel = before.guild.get_channel(get_channel_id('log'))
        if log_channel:
            await log_channel.send(embed=log_message_edit_em(before, after))


def setup(bot):
    bot.add_cog(Moderacja(bot))
