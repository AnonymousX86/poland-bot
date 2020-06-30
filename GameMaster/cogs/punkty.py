# -*- coding: utf-8 -*-
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import error_em, success_em
from GameMaster.templates.points import profile_em, ranking_em
from GameMaster.utils.database.points import get_points, add_points, remove_points, get_all_points
from GameMaster.utils.users import check_mention


class Punkty(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='profil',
        brief='Pokazuje profil z punktami użytkownika.',
        aliases=['profile', 'prof']
    )
    async def profil(self, ctx, user=None):
        user_id = check_mention(user) if user else ctx.message.author.id
        if user_id:
            member = ctx.guild.get_member(user_id)
            if member:
                points = get_points(user_id)
                await ctx.send(embed=profile_em(member, points))
            else:
                await ctx.send(embed=error_em('Taki użytkownik nie znajduje się na tym serwerze.'))
        else:
            await ctx.send(embed=error_em('Błędnie podałeś(aś) użytkownika.'))

    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(
        name='punkty',
        brief='Zarządza punktami.',
        usage='<użytkownik> <opcja> <punkty>',
        aliases=['points', 'pkt']
    )
    async def punkty(self, ctx, user=None, option=None, amount=None):
        if not user:
            await ctx.send(embed=error_em('Nie podałeś użytkownika.'))

        elif not option:
            await ctx.send(ebmed=error_em('Nie podałeś opcji.'))

        elif option not in ['+', '-']:
            await ctx.send(embed=error_em('Błędna opcja.'))

        elif not amount:
            await ctx.send(embed=error_em('Nie podałeś wartości punktów.'))

        elif amount == 0:
            await ctx.send(embed=error_em('Musisz podać liczbę różną od zera.'))

        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send(embed=error_em('Błędna wartość.'))
            else:
                user_id = check_mention(user)
                if not user_id:
                    await ctx.send(embed=error_em('Błędnie podany użytkownik.'))
                else:
                    member = ctx.guild.get_member(user_id)
                    if not member:
                        await ctx.send(embed=error_em('Ten użytkownik nie znajduje się na tym serwerze.'))
                    else:
                        func = add_points if option == '+' else remove_points
                        func(user_id, amount)
                        await ctx.send(embed=success_em(f'Punkty użytkownika **{member.display_name}**,'
                                                        f' zostały zaktualizowane.'))

    @command(
        name='ranking',
        brief='Tablica użytkowników.',
        description='Pokazuje użytkowników z największą ilością punktów.'
    )
    async def ranking(self, ctx):
        points = get_all_points()
        text = ''
        for i in points:
            if i[1]:
                try:
                    text += f'{ctx.guild.get_member(i[0]).mention}  -  {i[1]}\n'
                except AttributeError:
                    text += f'`{i[0]}`  -  {i[1]}\n'
        await ctx.send(embed=ranking_em(text))


def setup(bot):
    bot.add_cog(Punkty(bot))
