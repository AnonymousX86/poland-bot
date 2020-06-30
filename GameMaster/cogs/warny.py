# -*- coding: utf-8 -*-
from discord import Forbidden, HTTPException
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import success_em, error_em, please_wait_em
from GameMaster.templates.other import warns_em
from GameMaster.utils.database.warns import *
from GameMaster.utils.users import *


class Warny(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='warn',
        brief='Dodaje ostrzeżenie.',
        help='Maksymalnie 3 ostrzeżenia, 4 jest automatycznie zamienianie na ban.',
        usage='<użytkownik> [powód]',
        aliases=['addwarn']
    )
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def warn(self, ctx, user_id=None, *, reason='Brak'):
        if user_id is not None:
            user_id = check_mention(user_id)
            if user_id:
                user = self.bot.get_user(user_id)
                if user is not None:
                    warns = get_warn(user_id)
                    if len(warns) > 0:
                        count = warns[0][1] + 1
                    else:
                        count = 1
                    add_warn(user_id, reason)
                    if count <= 3:
                        member = ctx.guild.get_member(user_id)
                        try:
                            await member.add_roles(ctx.guild.get_role(warn_roles_ids[count]))
                        except AttributeError:
                            pass
                        await ctx.send(embed=success_em(
                            f'Ostrzeżono: **{user.name}**.\n'
                            f'Powód: **{reason if reason else "Brak"}**.\n'
                            f'To jest **{count}** ostrzeżenie.'
                        ))
                        try:
                            await user.send(embed=error_em(
                                f' Powód:```\n{reason if reason else "Brak"}```To Twoje **{count}** ostrzeżenie.',
                                ':exclamation: Zostałeś ostrzeżony(a)!'
                            ))
                        except Forbidden:
                            await ctx.send(embed=error_em(
                                f'Użytkownik **{user}** zablokował mnie (warto to zapisać).',
                                ':no_entry: Ojć!'
                            ))
                        except HTTPException:
                            await ctx.send(embed=error_em(
                                f'Nie mogę wysłać do **{user}** wiadomości przez problem z Discordem.'
                            ))
                    else:
                        await ctx.guild.ban(
                            user=user,
                            reason='Przekroczenie 3 ostrzeżeń',
                            delete_message_days=3
                        )
                        await ctx.send(embed=error_em(
                            f'Użytkownik {user.name} został zbanowany.',
                            title=':no_entry: Koniec ostrzeżeń'
                        ))
                        del_warns(user_id)
                else:
                    await ctx.send(embed=error_em('Nie znaleziono użytkownika.'))
            else:
                await ctx.send(embed=error_em('Błędny format komendy.'))
        else:
            await ctx.send(embed=error_em('Musisz podać, kogo chcesz upomnieć.'))

    @warn.error
    async def warn_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    @command(
        name='warns',
        brief='Lista ostrzeżeń.',
        help='Pokazuje kolejno:\n'
             '- ID ostrzeżenia,\n'
             '- nazwę użytkownika,\n'
             '- powód ostrzeżenia,\n'
             '- poziom ostrzeżenia,\n'
             '- date i godzinę.',
        aliases=['warnlist']
    )
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def warns(self, ctx):
        warns_records = get_warns()
        if len(warns_records) > 0:
            str_list = '```py\n'
            for record in warns_records.values():
                user = self.bot.get_user(int(record['user_id']))
                if user is not None:
                    user = '{0.display_name}#{0.discriminator}'.format(user)
                else:
                    user = f'{record["user_id"]}'
                if not record['warn_date'] or not record['warn_time']:
                    date_time = '-'
                else:
                    date_time = f'{record["warn_date"]} {record["warn_time"]}'
                if not record['warn_reason']:
                    reason = 'Brak'
                else:
                    reason = record['warn_reason']
                str_list += f'{record["warn_id"]}. {user}\n' \
                            f'   Powód: \' {reason} \'\n' \
                            f'   Liczba: {record["warn_level"]}  Data: {date_time}\n\n'
            str_list += '\n```'
            await ctx.send(embed=warns_em(str_list))
        else:
            await ctx.send(embed=error_em('Brak ostrzeżeń.'))

    @warns.error
    async def warns_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    @command(
        name='updatewarn',
        brief='Aktualizacja powodu ostrzeżenia.',
        help='Użyj argumentu "wszyscy" lub "all", aby zaktualizować role. Uwaga! Ta komenda nie powoduje usunięcia ról'
             ' osobom, które nie zostały ostrzeżone, a posiadają rolę o ostrzeżeniu',
        usage='<użytkownik> <powód>',
        aliases=['uwarn', 'changewarn']
    )
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def uwarn(self, ctx, user_id=None, *, reason=None):
        if user_id is not None:
            if user_id not in ['all', 'wszyscy']:
                if reason is not None:
                    if len(reason) <= 30:
                        user_id = check_mention(user_id)
                        if user_id:
                            user = self.bot.get_user(user_id)
                            if user is not None:
                                update_warn(user_id, reason)
                                await ctx.send(
                                    embed=success_em(f'Opis ostrzeżenia dla **{user.name}** został zaktualizowany.'
                                                     f'```{reason}```'))
                            else:
                                await ctx.send(embed=error_em('Nie mogę znaleźć takiego użytkownika.'))
                        else:
                            await ctx.send(embed=error_em('Błędny format komendy.'))
                    else:
                        await ctx.send(embed=error_em('Maksymalna długość powodu ostrzeżenia to **30 znaków**.'))
                else:
                    await ctx.send(embed=error_em('Nie podałeś(aś) powodu.'))
            else:
                count = 0
                msg = await ctx.send(embed=please_wait_em())
                for record in get_warns():
                    member = ctx.guild.get_member(record[0])
                    if member is not None:
                        count += 1
                        for role in range(3):
                            try:
                                warn_role = ctx.guild.get_role(warn_roles_ids[role + 1])
                                if role < record[1]:
                                    await member.add_roles(
                                        warn_role,
                                        reason=f'Użytkownik posiada {record[1]} poziom ostrzeżeń.'
                                    )
                                else:
                                    await member.remove_roles(
                                        warn_role,
                                        reason=f'Użytkownik posiada {record[1]} poziom ostrzeżeń.'
                                    )
                            except Forbidden:
                                await msg.edit(embed=error_em('Nie mam uprawnień do zmiany ról!'))
                            finally:
                                print(member.display_name)
                await msg.edit(embed=success_em(f'Zaktualizowani użytkownicy: **{count}**'))
        else:
            await ctx.send(embed=error_em('Nie podałeś(aś) użytkownika.'))

    @uwarn.error
    async def uwarn_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)

    @command(
        name='deletewarn',
        brief='Usuwanie ostrzeżeń.',
        description='Usuwa wszystkie ostrzeżenia, danemu użytkownikowi.',
        usage='<użytkownik>',
        aliases=['delwarn', 'dwarn']
    )
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def dwarn(self, ctx, user_id=None):
        if user_id is not None:
            user_id = check_mention(user_id)
            if user_id:
                del_warns(user_id)
                user = self.bot.get_user(user_id)
                member = ctx.guild.get_member(user_id)
                if member:
                    for i in range(3):
                        try:
                            await member.remove_roles(ctx.guild.get_role(warn_roles_ids[i + 1]))
                        except AttributeError:
                            pass
                await ctx.send(embed=success_em(
                    f'Usunięto ostrzeżenia użytkownikowi **{user.mention if user else f"`{user_id}`"}**.'))
            else:
                await ctx.send(embed=error_em('Błędny format komendy.'))
        else:
            await ctx.send(embed=error_em('Nie podałeś(aś) użytkownika.'))

    @dwarn.error
    async def dwarn_error(self, ctx, error):
        await self.bot.error_msg(ctx, error)


def setup(bot):
    bot.add_cog(Warny(bot))
