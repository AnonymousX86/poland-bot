    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(
        name='kick',
        brief='Wyrzuca z serwera.',
        usage='<użytkownik>'
    )
    async def kick(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo wyrzucić.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                member = ctx.guild.get_member(user_id)
                if not member:
                    await ctx.send(embed=error_em('Ten użytkownik nie znajduje się na serwerze.'))
                else:
                    try:
                        await member.kick(reason=f'Wyrzucony przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas wyrzucania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie wyrzucono **{member}**.'))

    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(
        name='ban',
        brief='Banuje z serwera.',
        usage='<użytkownik>'
    )
    async def ban(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo zbanować.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                member = ctx.guild.get_member(user_id)
                if not member:
                    await ctx.send(embed=error_em('Ten użytkownik nie znajduje się na serwerze.'))
                else:
                    try:
                        await member.ban(reason=f'Zbanowany przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas banowania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie zbanowano **{member}**.'))

    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(
        name='unban',
        brief='Usuwa ban z serwera.',
        usage='<użytkownik>'
    )
    async def unban(self, ctx, mention):
        if not mention:
            await ctx.send(embed=error_em('Nie podałeś(aś) kogo odbanować.'))
        else:
            user_id = check_mention(mention)
            if not user_id:
                await ctx.send(embed=error_em('Błędny format komendy.'))
            else:
                try:
                    user = await self.bot.fetch_user(user_id)
                except NotFound:
                    await ctx.send(embed=error_em('Ten użytkownik nie istnieje.'))
                else:
                    try:
                        await user.unban(reason=f'Odbanowany przez: {ctx.author}')
                    except HTTPException:
                        await ctx.send(embed=error_em('Błąd podczas odbanowania.'))
                    else:
                        await ctx.send(success_em(f'Pomyślnie odbanowano **{user}**.'))

