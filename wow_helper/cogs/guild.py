import discord
from discord.ext import commands

from wow_helper import utils
from wow_helper import config
from wow_helper import db

logger = utils.get_logger(__name__)


class Guild(commands.Cog):
    """Commands relating to wow guild assignment operations."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Update WoW guild name.', aliases=['setguild', 'guildname'])
    @commands.has_permissions(administrator=True)
    async def guild(self, ctx: commands.Context) -> None:
        logger.info(f'Updating WoW guild for Discord guild {ctx.guild.id}')

        await ctx.message.author.send('Please enter your wow guild name, be sure to enclose it in quotes if it is more than one word!')
        name = await ctx.bot.wait_for('message')

        await ctx.message.author.send('Please enter your wow server name, be sure to enclose it in quotes if it is more than one word!')
        server = await ctx.bot.wait_for('message')

        if name == "":
            name = None
        if server == "":
            server = None

        db.update_guild(ctx.guild.id, wow_name=name.content, wow_server=server.content)
        embed = discord.Embed(title='WoW Guild Set!')
        embed.add_field(name='Congrats!', value='With this set, you can now automatically query data for your guild!')
        logger.info('Successfully updated guild data.')

    @guild.error
    async def guild_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        logger.error(f'{error}')
        await ctx.send(f'Usage: {config.bot_prefix()}guild "[GUILD NAME]" [SERVER]')
