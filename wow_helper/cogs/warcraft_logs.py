import asyncio
from typing import Union
import discord
import requests
from discord.ext import commands

from wow_helper import utils, config, db
from wow_helper.api.warcraft_logs_api import WarcraftLogsAPI

logger = utils.get_logger(__name__)

DEFAULT_REGION = 'us'


class WarcraftLogs(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Check character parse data.', aliases=['get-parses', 'my-parses'])
    async def parses(self, ctx: commands.Context, name: Union[str, None], *, realm: Union[str, None]) -> None:
        api = WarcraftLogsAPI()

        # TODO: Make this a callable function
        if name is None and realm is None:
            char_info = db.get_user_information(ctx.author.id)
        elif name is None or realm is None:
            logger.error('Improper usage of score command.')
            await ctx.send(f'Usage: {config.bot_prefix()}parses CHARACTER REALM')
            return
        else:
            char_info = (name, realm, DEFAULT_REGION)

        if char_info is None:
            logger.error(f'Could not find information for user {ctx.author.id}.')
            await ctx.send('Be sure to use the command /set-character before executing this command with no arguments.')
            return

        char_info = (char_info[0].lower(), char_info[1].lower().replace(' ', '-'), char_info[2])

        response = api.get_character_parses(char_info[0], char_info[1], char_info[2])

        logger.debug(response)
