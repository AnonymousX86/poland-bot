# -*- coding: utf-8 -*-
from discord import Message, Embed, Color


def _log_message_add_info(embed: Embed, message: Message) -> Embed:
    return embed.add_field(
        name='Autor',
        value=message.author
    ).add_field(
        name='Kanał',
        value=message.channel
    ).add_field(
        name='Czas wysłania',
        value=message.created_at
    )


def log_message_del_em(message: Message) -> Embed:
    return _log_message_add_info(Embed(
        title='Wiadomość usunięta',
        description=f'```\n{message.content}\n```',
        color=Color.red()
    ), message)


def log_message_edit_em(before: Message, after: Message) -> Embed:
    return _log_message_add_info(Embed(
        title='Wiadomość edytowana',
        description=f'Przed:```\n{before}\n```Po:```\n{after}\n```'
    ), before)
