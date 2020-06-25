# -*- coding: utf-8 -*-
from random import randint, choice, seed

from discord.ext.commands import Cog, command

from GameMaster.templates.basic import error_em
from GameMaster.templates.other import member_em
from GameMaster.templates.random import dice_em, choose_em, eight_ball_em, rate_em


class Losowe(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='kostka',
        brief='Rzuca kością.',
        description='Może rzucić różną ilością kości o różnych ilościach ścianek.',
        help='Ściany kostki muszą być co najmniej cztery, a rzut przynajmniej jeden.'
             ' Domyślnymi wartościami są: 6 (ściany) i 1 (rzut).'
             ' Dodatkowo można dodać własny separator (domyślnie ", ").',
        aliases=['kość', 'k'],
        usage='[ściany] [rzuty] [separator]'
    )
    async def kostka(self, ctx, k=6, x=1, sep=', '):
        try:
            k = int(k)
            x = int(x)
        except ValueError:
            await ctx.send(embed=error_em('Podane wartości muszą być liczbami.'))
        else:
            if k < 4:
                await ctx.send(embed=error_em('Liczba ścianek musi wynosić co najmniej 4.'))
            elif x < 1:
                await ctx.send(embed=error_em('Liczba rzutów musi być dodatnia.'))
            elif k > 100 or x > 100:
                await ctx.send(embed=error_em('Zbyt duże wartości!'))
            else:
                result = []
                for i in range(x):
                    result.append(str(randint(1, k)))
                await ctx.send(embed=dice_em(result, sep))

    @command(
        name='losowy',
        brief='Wybiera losowego użytkownika.',
        description='Wyświetlane są nazwa, zdjęcie, status i nick losowego użytkownika z serwera.',
        usage='[rola|ID roli]'
    )
    async def losowy(self, ctx, arg=None):
        role_id = 0
        member = None

        if arg:
            # Role ID only
            if len(arg) == 18:
                try:
                    role_id = int(arg)
                except ValueError:
                    pass
            # Role mention
            elif len(arg) == 21:
                role_id = int(arg[3:-1])
            role = ctx.guild.get_role(role_id)
            if not role:
                # User mention
                if len(arg) == 22:
                    member = ctx.guild.get_member(int(arg[3:-1]))
        else:
            role = ctx.guild.default_role

        if member:
            await ctx.send(mebed=member_em(member))
        elif role:
            possibles = [member for member in ctx.guild.members if role in member.roles]
            if possibles:
                await ctx.send(
                    embed=member_em(choice(possibles)).set_footer(text=f'Wylosowany(a) z grupy {role.name}.'))
            else:
                await ctx.send(embed=error_em(f'Nie mogę znaleźć nikogo z rolą {role.mention}.'))
        else:
            await ctx.send(embed=error_em('Nie ma takiej roli.'))

    @command(
        name='wybierz',
        brief='Pomaga w wyborze.',
        description='Wybiera spomiędzy wprowadzonych rzeczy.',
        help='Oddzielaj pozycje przecinkami ze spacją. (", ")',
        usage='<coś 1>, <coś 2>, ... [coś n]'
    )
    async def wybierz(self, ctx, *, things=None):
        if not things:
            await ctx.send(embed=error_em('Nie podałeś nic.'))
        else:
            things = things.split(', ')
            if len(things) < 2:
                await ctx.send(embed=error_em('Podaj co najmniej 2 rzeczy.'))
            else:
                await ctx.send(embed=choose_em(':arrow_right:', choice(things)))

    @command(
        name='moneta',
        brief='Rzuca monetą.',
        description='Istnieje szansa 0,9%, że moneta stanie na krawędzi oraz 0,1%, że zniknie.'
                    ' Zgodnie z założeniami fizyki kwantowej.'
    )
    async def moneta(self, ctx):
        lot = randint(1, 1000)
        if lot <= 1:
            result = [':face_with_raised_eyebrow:', 'Moneta znikła']
        elif lot <= 10:
            result = [':exploding_head:', 'Moneta stanęła na krawędzi']
        elif lot <= 505:
            result = [':arrow_heading_down:', 'Orzeł']
        else:
            result = [':arrow_heading_up:', 'Reszka']
        await ctx.send(embed=choose_em(result[0], result[1]))


def setup(bot):
    bot.add_cog(Losowe(bot))
