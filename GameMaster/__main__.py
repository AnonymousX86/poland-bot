# -*- coding: utf-8 -*-
from logging import basicConfig, INFO
from os import getenv

from discord import Status, Activity, ActivityType
from discord.ext.commands import Bot, ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, \
    MissingPermissions, BotMissingPermissions
from nest_asyncio import apply

from GameMaster.utils.database import check_connection
from GameMaster.utils.templates import error_em
from settings import bot_token


class CheckDatabaseError(BaseException):
    pass


apply()

basicConfig(level=INFO)

bot = Bot(
    command_prefix='$',
    case_insensitive=False,
    owner_id=309270832683679745,
    description='Bot serwera Poland.'
)


@bot.event
async def on_ready():
    print('Logged in as: {0} ({0.id})'.format(bot.user))

    if not check_connection():
        raise CheckDatabaseError('Can\'t check connection to PostgreSQL.')
    else:
        print('PostgreSQL connection OK')

    status = Status.online
    ac = 'Kości'
    if getenv('LOCALAPPDATA') == 'C:\\Users\\Kubas\\AppData\\Local':
        ac += ' (w produkcji)'
    activity = Activity(type=ActivityType.playing, name=ac)
    await bot.change_presence(status=status, activity=activity)


async def error_msg(ctx, error):
    if isinstance(error, MissingPermissions):
        status = 'Nieuprawnionym wstęp wzbroniony!'

    elif isinstance(error, BotMissingPermissions):
        status = 'Nie posiadam uprawnień!'

    else:
        status = f'```py\n{error.__class__.__name__}: {error}```'

    await ctx.send(embed=error_em(status))


bot.error_msg = error_msg

cogs = (
    'GameMaster.cogs.warny',
    'GameMaster.cogs.czyszczenie',
    'GameMaster.cogs.losowe'
)
for cog in cogs:
    p = '[COGS]'
    try:
        bot.load_extension(cog)
        print(f'{p} Loaded: {cog}')
    except ExtensionNotFound:
        print(f'{p} Not found: {cog}')
    except ExtensionAlreadyLoaded:
        print(f'{p} Already loaded: {cog}')
    except NoEntryPointError:
        print(f'{p} Cog "{cog}" do not have "setup()" function')
    except Exception as e:
        print(f'{p} {e.__class__.__name__}: {e}')

bot.run(bot_token())
