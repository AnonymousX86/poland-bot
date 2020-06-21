# -*- coding: utf-8 -*-
from discord import Forbidden, HTTPException
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import info_em, error_em, success_em, please_wait_em
from GameMaster.utils.database import purge_enabled, purge_settings, purge_enable, purge_disable


class Purge(Cog):
    def __init__(self, bot):
        self.bot = bot

    settings = {}

    @has_permissions(kick_members=True, manage_roles=True)
    @bot_has_permissions(kick_members=True, manage_roles=True)
    @command(
        name='purge',
        brief='Główna komenda czystki.',
        description='Włącza czystkę, wysyłając odpowiednią wiadomość na ustawiony kanał. Po otrzymaniu wiadomości'
                    ' dodaje rangę aktywnego. Po zakończeniu wyrzuca osoby z rangą nieaktywnego.',
        help='Dostępne opcje: start (domyślna), status, update, stop.',
        aliases=['czystka'],
        usage='[opcja]'
    )
    async def purge(self, ctx, option='start'):
        option = option.lower()
        if option in ['start', 'status', 'update', 'stop']:
            gid = ctx.guild.id
            self.settings = purge_settings(gid)
            active_role = ctx.guild.get_role(self.settings['active_role_id'])
            inactive_role = ctx.guild.get_role(self.settings['inactive_role_id'])
            purge_on = purge_enabled(gid)

            if option == 'start':
                if not purge_on:
                    await ctx.guild.get_channel(self.settings['check_channel_id']).send(
                        embed=info_em('Rozpoczęcie czystki. Proszę napisz dowolną wiadomość na tym kanale.')
                    )
                    purge_enable(gid)
                    self.bot.add_listener(self.purge_listener, 'on_message')
                    await ctx.send(embed=success_em(
                        f'Czystka włączona na kanale'
                        f' {ctx.guild.get_channel(self.settings["check_channel_id"]).mention}.'
                    ))
                else:
                    await ctx.send(embed=error_em('Czystka jest już włączona lub błąd ustawień.'))

            elif option == 'status':
                if purge_on:
                    active = 0
                    inactive = 0
                    for member in ctx.guild.members:
                        if not member.bot:
                            if active_role in member.roles:
                                active += 1
                            elif inactive_role in member.roles:
                                inactive += 1
                    await ctx.send(embed=info_em(
                        f'Aktywni: **{active}**\n'
                        f'Nieaktywni: **{inactive}**'
                    ))
                else:
                    await ctx.send(embed=error_em('Czystka nie jest włączona lub błąd ustawień.'))

            elif option == 'update':
                if purge_on:
                    msg = await ctx.send(embed=please_wait_em())
                    inactive = 0
                    for index, member in enumerate(ctx.guild.members):
                        if not member.bot:
                            if active_role not in member.roles:
                                await member.add_roles(inactive_role, reason='Czystka')
                                inactive += 1
                                print(f'Added to: {member}')
                        if index % 10 == 0:
                            await msg.edit(embed=please_wait_em(
                                f'({inactive})'
                                f'**{len(ctx.guild.members) // index}%**'
                            ))
                    await msg.edit(embed=success_em(f'Dodane role `@nieaktywny`: **{inactive}**.'))
                else:
                    await ctx.send(embed=error_em('Czystka nie jest włączona lub błąd ustawień.'))

            elif option == 'stop':
                if purge_enabled(gid):
                    msg = await ctx.send(embed=please_wait_em())
                    kicked = 0
                    unable = 0
                    for member in ctx.guild.members:
                        if inactive_role in member.roles:
                            try:
                                await member.kick(reason='Czystka')
                            except Forbidden or HTTPException:
                                unable += 1
                            else:
                                kicked += 1
                    await msg.edit(embed=success_em(
                        f'Wyrzucono: **{kicked}**\n'
                        f'Niepowodzenia: **{unable}**\n'
                        f'Czystkę rozpoczęto: **{self.settings["purge_started_date"]}**'
                    ))
                    purge_disable(gid)
                    self.bot.remove_listener(self.purge_listener, 'on_message')
                else:
                    await ctx.send(embed=error_em('Czystka jest wyłączona lub błąd ustawień.'))

        else:
            await ctx.send(embed=error_em('Błędny argument'))

    @purge.error
    async def purge_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    async def purge_listener(self, message):
        if message.channel.id == self.settings['check_channel_id']:
            try:
                await message.guild.get_member(message.author.id).add_roles(
                    message.guild.get_role(self.settings['active_role_id']),
                    reason=f'Napisał(a) na kanale {message.guild.get_channel(self.settings["check_channel_id"]).name}'
                )
                await message.guild.get_member(message.author.id).remove_roles(
                    message.guild.get_role(self.settings['active_role_id']),
                    reason=f'Napisał(a) na kanale {message.guild.get_channel(self.settings["check_channel_id"]).name}'
                )
            except HTTPException:
                await message.channel.send(embed=error_em(f'Nie mogę zatwierdzić **{message.author.name}**.'))


def setup(bot):
    bot.add_cog(Purge(bot))
