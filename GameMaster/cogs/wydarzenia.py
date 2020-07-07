# -*- coding: utf-8 -*-
from discord import Message, Reaction, User, Guild, TextChannel
from discord.ext.commands import Cog, command, Context, has_permissions

from GameMaster.templates.basic import success_em, error_em
from GameMaster.templates.events import event_confirm_em, new_event_em
from settings import get_channel_id


class Wydarzenia(Cog):
    def __init__(self, bot):
        self.bot = bot

    msg: Message = None
    raw_text: str = None
    starter: User = None
    emoji_up = '\U0001f44d'
    emoji_down = '\U0001f44e'

    async def _rm_reaction_listener(self):
        self.bot.remove_listener(self.wiat_for_reaction_response)
        await self.msg.clear_reactions()

    async def _event_confirm(self, guild: Guild):
        e = new_event_em(self.raw_text)
        channel_1: TextChannel = guild.get_channel(get_channel_id('screeny'))
        await channel_1.send(embed=e)
        channel_2: TextChannel = guild.get_channel(get_channel_id('event'))
        await channel_2.send(embed=e)

    @has_permissions(manage_guild=True)
    @command(
        name='event',
        brief='Zarządzanie wydarzeniami.'
    )
    async def event(self, ctx: Context, option: str, *, title: str):
        if option not in ['nowy', 'n']:
            await ctx.send(embed=error_em('Błędna opcja.'))
        elif not title:
            await ctx.send(embed=error_em('Brak tematu.'))
        else:
            self.msg = await ctx.send(embed=event_confirm_em(title))
            self.raw_text = title
            self.starter: User = ctx.author
            try:
                await self.msg.add_reaction(self.emoji_up)
                await self.msg.add_reaction(self.emoji_down)
            finally:
                self.bot.add_listener(self.wiat_for_reaction_response, 'on_reaction_add')

    @event.error
    async def event_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    async def wiat_for_reaction_response(self, reaction: Reaction, user: User):
        if user == self.starter and reaction.count > 1 and reaction.message.id == self.msg.id:
            if reaction.emoji == self.emoji_up:
                await self._rm_reaction_listener()
                await self.msg.edit(embed=success_em(
                    'Wiadomość zatwierdzona.'
                ))
                await self._event_confirm(reaction.message.guild)
            elif reaction.emoji == self.emoji_down:
                await self._rm_reaction_listener()
                await self.msg.edit(embed=success_em(
                    'Wysyłanie wiadomości zostało anulowane.'
                ))


def setup(bot):
    bot.add_cog(Wydarzenia(bot))
