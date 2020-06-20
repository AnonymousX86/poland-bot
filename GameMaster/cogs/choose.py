#-*- coding: utf-8 -*-
from random import randint, choice, floor

from discord import HTTPException
from discord.ext.commands import Cog, command

from GameMaster.templates.random import choose_em
from GameMaster.templates.basic import error_em


class Choose(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='wybierz',
        brief='Wybiera jedną z podanych rzeczy.',
        aliases=['ch', 'choose'],
        usage='[rzeczy przedzielone przecinkiem]'
    )
    
    async def choose(self, ctx, *, arg):
      if len(arg) == 0:
         await ctx.send(embed=error_em('Musisz podać minimum 2 rzeczy przedzielone przecinkiem!'));
         
      wiadomosci = arg.split(', ');
      if len(wiadomosci) == 1:
        await ctx.send(embed=error_em('Musisz podać minimum 2 rzeczy przedzielone przecinkiem!'));
        
      x = floor(random()* len(wiadomosci));
      rzecz = wiadomosci[x-1];
      
      await ctx.send(embed=choose_em(rzecz));
      
def setup(bot):
    bot.add_cog(Choose(bot))
