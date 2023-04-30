import discord
from discord.ext import commands

from wow_helper import utils
from wow_helper import config
from wow_helper import db

logger = utils.get_logger(__name__)


class User(commands.Cog):
    """Commands relating to wow guild assignment operations."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Update WoW player name.', aliases=['set-character', 'character-name', 'register'])
    @commands.has_permissions(administrator=True)
    async def register_user(self, ctx: commands.Context) -> None:
        logger.info(f'Updating WoW player name for Discord guild {ctx.guild.id}')

        await ctx.message.author.send('Please enter your WoW character name.')
        name = await ctx.bot.wait_for('message')

        await ctx.message.author.send('Please enter your WoW server name.')
        server = await ctx.bot.wait_for('message')

        if name == '':
            name = None
        if server == '':
            server = None

        db.insert_or_update_user(ctx.author.id, ctx.guild.id, ctx.author.name, wow_name=name.content, wow_server=server.content) # need to insert if no exist update if exist
        embed = discord.Embed(title='WoW Character Name Set!')
        embed.add_field(name='Congrats!', value='With this set, you can now automatically query data for your character!')
        logger.info(f'Successfully updated user data for user {ctx.author.id} on guild {ctx.guild.id}.')
