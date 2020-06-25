# -*- coding: utf-8 -*-
from logging import basicConfig, INFO
from os import getenv

from discord import Status, Activity, ActivityType
from discord.ext.commands import Bot, ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, \
    MissingPermissions, BotMissingPermissions
from nest_asyncio import apply as async_apply

from GameMaster.templates.basic import error_em
from GameMaster.utils.database.basic import check_connection
from settings import get_bot_token


async def error_msg(ctx, error):
    if isinstance(error, MissingPermissions):
        s = 'Nieuprawnionym wstęp wzbroniony!'

    elif isinstance(error, BotMissingPermissions):
        s = 'Nie posiadam uprawnień!'

    else:
        s = f'```py\n{error.__class__.__name__}: {error}```'

    await ctx.send(embed=error_em(s))


if __name__ == '__main__':
    async_apply()
    basicConfig(level=INFO)

    bot = Bot(
        command_prefix='$',
        case_insensitive=False,
        description='Bot serwera Poland.',
        owner_id=309270832683679745,
    )


    @bot.event
    async def on_ready():
        print('[Bot] Logged in as: {0} ({0.id})'.format(bot.user))

        p = '[Database]'
        if check_connection():
            print(f'{p} Connection OK')
        else:
            print(f'{p} Can\'t connect')

        status = Status.online
        ac = 'Kości'
        if getenv('LOCALAPPDATA') == 'C:\\Users\\Kubas\\AppData\\Local':
            ac += ' (w produkcji)'
        activity = Activity(type=ActivityType.playing, name=ac)
        await bot.change_presence(status=status, activity=activity)

        bot.error_msg = error_msg

        for cog in [f'GameMaster.cogs.{cog}' for cog in [
            'czystka',
            'losowe',
            'podstawowe',
            'poziomy',
            'warny',
            'zabawne'
        ]]:
            p = '[Cogs]'
            try:
                bot.load_extension(cog)
                print(f'{p} Loaded: {cog}')
            except ExtensionNotFound:
                print(f'{p} Not found: {cog}')
            except ExtensionAlreadyLoaded:
                print(f'{p} Already loaded: {cog}')
            except NoEntryPointError:
                print(f'{p} Extension "{cog}" do not have "setup()" function')
            except Exception as e:
                print(f'{p} {e.__class__.__name__}: {e}')

        bot.history = {
            'last_8ball': ''
        }


    bot.run(get_bot_token())
