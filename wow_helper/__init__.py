import sys
import discord
from discord.ext import commands

from wow_helper import config, utils, cogs, events, db

"""
Secondary entry point for the bot. This module stores information relating to the main function and some extension setup
prior to starting execution.
"""

logger = utils.get_logger(__name__)

print(r"""
 __      __ __      __   _  _     _               
 \ \    / /_\ \    / /__| || |___| |_ __  ___ _ _ 
  \ \/\/ / _ \ \/\/ /___| __ / -_) | '_ \/ -_) '_|
   \_/\_/\___/\_/\_/    |_||_\___|_| .__/\___|_|  
                                   |_|            
""")
logger.info(f"Starting WoW-Helper version {utils.version()}.")
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=config.bot_prefix())


@bot.event
async def on_ready() -> None:
    db.instantiate_tables()
    for guild in bot.guilds:
        db.insert_guild(guild.id, guild.name)
    logger.info(f'Loading extensions...')
    events.setup(bot)
    await cogs.setup(bot)
    logger.info(f'WoW-Helper is ready to run.')


def main() -> None:
    try:
        bot.run(config.bot_token())
    except discord.errors.LoginFailure as e:
        logger.error(e)
        sys.exit(2)
