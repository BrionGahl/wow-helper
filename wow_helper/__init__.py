import sys

import discord
from discord.ext import commands

from wow_helper import config
from wow_helper import utils
from wow_helper import cogs
from wow_helper import events

logger = utils.get_logger(__name__)

print("""
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
    logger.info(f'Loading extensions...')
    events.__init__(bot)
    await cogs.setup(bot)
    logger.info(f'WoW-Helper is ready to run.')


def main() -> None:
    try:
        bot.run(config.bot_token())
    except Exception as e:
        logger.error("Failed to connect to DiscordAPI.")
        print(e)
        sys.exit(2)
