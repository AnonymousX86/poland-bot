# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog, command, has_permissions, bot_has_permissions

from GameMaster.templates.basic import error_em, success_em
from GameMaster.templates.points import ranking_em
from GameMaster.templates.users import profile_em
from GameMaster.utils.database.points import add_points, remove_points, get_all_points
from GameMaster.utils.database.users import del_user, add_user
from GameMaster.utils.general import sort_nested
from GameMaster.utils.ranking import nth_place
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
                await ctx.send(embed=profile_em(member))
            else:
                await ctx.send(embed=error_em('Taki użytkownik nie znajduje się na tym serwerze.'))
        else:
            await ctx.send(embed=error_em('Błędnie podałeś(aś) użytkownika.'))

    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(
        name='punkty',
        brief='Zarządza punktami.',
        help='Dostępne opcje to "+" (dodawanie) i "-" (odejmowanie).',
        usage='<użytkownik> <opcja> <punkty>',
        aliases=['points', 'pkt']
    )
    async def punkty(self, ctx, user=None, option_human=None, amount=None):
        if not user:
            await ctx.send(embed=error_em('Nie podałeś użytkownika.'))

        elif not option_human:
            await ctx.send(embed=error_em('Nie podałeś opcji.'))

        elif option_human not in ['+', '-']:
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
                        func = add_points if option_human == '+' else remove_points
                        func(user_id, amount)
                        option_human = 'Dodano' if option_human == '+' else 'Odjęto'
                        await ctx.send(embed=success_em(
                            f'Punkty użytkownika **{member.display_name}** zostały zaktualizowane.\n'
                            f'**{option_human}** punkty w ilości: **{amount}**.'
                        ))

    @command(
        name='ranking',
        brief='Tablica użytkowników.',
        description='Pokazuje użytkowników z największą ilością punktów.'
    )
    async def ranking(self, ctx):
        points = sort_nested(get_all_points(), reversed_=True)
        text = ''
        for i, p in enumerate(points, start=1):
            member = ctx.guild.get_member(p[0])
            if not member:
                member = f'`{p[0]}`'
            else:
                member = member.mention
            if p[1]:
                text += f'{nth_place(i)} {member}  -  {p[1]}\n'
        await ctx.send(embed=ranking_em(text))

    @Cog.listener(
        name='on_member_remove'
    )
    async def db_profile_remover(self, member: Member):
        del_user(member.id)

    @Cog.listener(
        name='on_member_join'
    )
    async def db_profile_adder(self, member: Member):
        add_user(member.id)


def setup(bot):
    bot.add_cog(Punkty(bot))
