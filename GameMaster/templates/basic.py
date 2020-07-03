# -*- coding: utf-8 -*-
from discord import Color, Embed, Guild
from discord.ext.commands import Bot


def error_em(text, title=':red_circle: Błąd!', color=Color.red()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def success_em(text, title=':green_circle: Gotowe!', color=Color.green()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def please_wait_em(text='', title=':hourglass_flowing_sand: Daj mi chwilę...', color=Color.gold()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def info_em(text='', title=':information_source: Informacja', color=Color.blue()) -> Embed:
    return Embed(
        title=title,
        description=text,
        color=color
    )


def bot_info_em(bot: Bot) -> Embed:
    return Embed(
        title=bot.user.name,
        description='\u200b',
        color=Color.dark_red()
    ).add_field(
        name='Właściciel',
        value=bot.get_user(bot.owner_id)
    ).add_field(
        name='Wersja',
        value=bot.version or 'Nieznana'
    ).set_thumbnail(
        url=bot.user.avatar_url
    )


def guild_info_em(guild: Guild):
    return Embed(
        title=guild.name,
        description=guild.description or '\u200b',
        color=Color.dark_magenta()
    ).add_field(
        name='Użytkownicy',
        value=str(guild.member_count),
        inline=False
    ).add_field(
        name='Właściciel',
        value=f'{guild.owner}\nID: `{guild.owner_id}`',
        inline=False
    ).add_field(
        name='Utworzono',
        value=guild.created_at.strftime('%Y-%m-%d %H:%M'),
        inline=False
    ).add_field(
        name='Poziom Nitro Boost',
        value=guild.premium_tier,
        inline=False
    ).add_field(
        name='Kanały tekstowe, głosowe, kategorie',
        value=f'{len(guild.text_channels)}/{len(guild.voice_channels)}/{len(guild.categories)}',
        inline=False
    ).add_field(
        name='Region',
        value=str(guild.region).capitalize(),
        inline=False
    ).set_thumbnail(
        url=guild.icon_url
    )
