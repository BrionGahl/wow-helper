import asyncio

import discord
from discord.ext import commands

from wow_helper import utils, db

logger = utils.get_logger(__name__)


class User(commands.Cog):
    """Commands relating to wow guild assignment operations."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Update WoW player name.', aliases=['set-character', 'register-character', 'register'])
    async def register_user(self, ctx: commands.Context) -> None:
        logger.info(f'Updating WoW player name for Discord guild {ctx.guild.id}')
        reactions = {'🇺🇸': 'us', '🇪🇺': 'eu', '🇹🇼': 'tw', '🇰🇷': 'kr'}

        try:
            await ctx.message.author.send('Please enter your WoW character name.')
            name = await ctx.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel)

            await ctx.message.author.send('Please enter your WoW server name.')
            server = await ctx.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel)

            message = await ctx.message.author.send('Please react with the appropriate region.')
            for key, value in reactions.items():
                await message.add_reaction(key)

            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author and str(r.emoji) in reactions)
        except asyncio.TimeoutError:
            logger.error(f'Command timed out for user {ctx.author.id} on guild {ctx.guild.id}')
            await ctx.message.author.send('Command timed out...')
            return

        db.insert_or_update_user(ctx.author.id, ctx.guild.id, ctx.author.name, wow_name=name.content, wow_server=server.content, wow_region=reactions[reaction.emoji]) # need to insert if no exist update if exist
        embed = discord.Embed(title='WoW Character Name Set!')
        embed.add_field(name='Congrats!', value='With this set, you can now automatically query data for your character!', inline=False)
        embed.add_field(name=f'{name.content}', value=f'{server.content}, {reactions[reaction.emoji].upper()}', inline=False)

        await ctx.send(embed=embed)

        logger.info(f'Successfully updated user data for user {ctx.author.id} on guild {ctx.guild.id}.')
