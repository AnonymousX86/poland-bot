# -*- coding: utf-8 -*-
from random import seed, randint, choice

from discord.ext.commands import Cog, command

from GameMaster.templates.basic import error_em
from GameMaster.templates.random import eight_ball_em, rate_em


class Zabawne(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='8ball',
        brief='Kula tobie pomoże.',
        help='Pytania powinny zaczynać się od "czy", ponieważ oryginalna kula odpowiada na pytania:'
             ' "Czy powinienem (...) ?".',
        usage='<pytanie>'
    )
    async def eight_ball(self, ctx, *, question=None):
        if not question:
            await ctx.send(embed=error_em('Nie podałeś(aś) pytania.'))
        elif not question.endswith('?'):
            await ctx.send(embed=error_em('Pytania kończą się znakiem zapytania.'))
        elif len(question) < 10:
            await ctx.send(embed=error_em('Pytanie jest zbyt krótkie.'))
        else:
            while True:
                seed(question.lower())
                result = choice([
                    'Jasne że tak',
                    'Może lepiej nie',
                    'Chyba sobie żartujesz',
                    'Też nie wiem',
                    'Lepiej spytać sąsiada',
                    'Admin mówi że tak',
                    'Tak, ale św. Mikołajowi się to nie spodoba',
                    'Teoretycznie tak, a praktycznie nie',
                    'Trudne pytanie, muszę się chwilę zastanowić',
                    'A co za różnica',
                    'Nie, znaczy tak',
                    'Tak, ale nie chcę wiedzieć skąd to pytanie',
                    'A nie możesz samemu sobie odpowiedzieć',
                    'Proszę pomóż mi, jestem uwięziony w środku bota',
                    'Nie rozumiem',
                    'Spróbuj jeszcze raz',
                    'Pomyśl',
                    'Idę coś zjeść, będę za 15 minut',
                    'Nie mi oceniać',
                    'Ja też potrzebuję snu',
                    'Proszę przestań się mnie pytać o takie głupoty',
                    'Wciśnij Alt + F4',
                    'Jednorożce, tak to wszystko',
                    'Chyba nie myślisz, że serio pomogę',
                    'A co zrobiłby Jedi',
                    'To morderca',
                    'Żartujesz... Prawda?',
                    'Lepiej zapytaj się mnie, czy mnie to obchodzi',
                    'Na 100%',
                    'Tak, ale zrób to będąc nawalonym tak jak tylko potrafisz',
                    'Nie mogę teraz powiedzieć',
                    'Zależy',
                    'To nie jest OK',
                    'Odpowiedź znajdziesz po swojej prawej stronie'
                ])
                if result != self.bot.history['last_8ball']:
                    self.bot.history['last_8ball'] = result
                    break
            await ctx.send(embed=eight_ball_em(result))

    @command(
        name='oceń',
        brief='Wystawia ocenę.',
        description='Wystawia ocenę z zakresu od 1 do 10.',
        help='Ten sam przedmiot zawsze otrzyma taką samą ocenę.',
        usage='<przedmiot>',
        aliases=['rate']
    )
    async def rate(self, ctx, *, arg=None):
        if not arg:
            await ctx.send(embed=error_em('Musisz podać rzecz do ocenienia!'))
        else:
            arg = arg.lower()
            seed(arg)
            ocena = randint(1, 10)
            await ctx.send(embed=rate_em(arg, ocena))


def setup(bot):
    bot.add_cog(Zabawne(bot))
