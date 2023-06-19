import asyncio
from typing import Union
import discord
import requests
from discord.ext import commands

from wow_helper import utils, config, db
from wow_helper.api.warcraft_logs_api import WarcraftLogsAPI

logger = utils.get_logger(__name__)

ABERRUS_RAID_IMG = 'https://assets.rpglogs.com/img/warcraft/zones/zone-33.png'


class WarcraftLogs(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Check character parse data.', aliases=['get-parses', 'my-parses'])
    async def parses(self, ctx: commands.Context, name: Union[str, None], *, realm: Union[str, None]) -> None:
        raid_bosses = ['Kazzara', 'Amalgamation', 'Experiments', 'Assault', 'Rashok', 'Zskarn', 'Magmorax', 'Echo', 'Sarkareth']
        api = WarcraftLogsAPI()

        # TODO: Make this a callable function
        if name is None and realm is None:
            char_info = db.get_user_information(ctx.author.id)
        elif name is None or realm is None:
            logger.error('Improper usage of score command.')
            await ctx.send(f'Usage: {config.bot_prefix()}parses CHARACTER REALM')
            return
        else:
            char_info = (name, realm, config.default_region())

        if char_info is None:
            logger.error(f'Could not find information for user {ctx.author.id}.')
            await ctx.send('Be sure to use the command /set-character before executing this command with no arguments.')
            return

        char_info = (char_info[0].lower(), char_info[1].lower().replace(' ', '-').replace('\'', ''), char_info[2])

        response = api.get_character_parses(char_info[0], char_info[1], char_info[2])

        embed = discord.Embed(title=f'{char_info[0].title()}, {response.pop("guild")}')
        embed.set_author(name=f'WarcraftLog Parses')
        embed.set_thumbnail(url=ABERRUS_RAID_IMG)
        for index, key in enumerate(response):
            embed.add_field(name=f'{raid_bosses[index]}: {response[key][1]}', value=f'DPS: {response[key][0]} | HPS: {response[key][2]}', inline=False)

        await ctx.send(embed=embed)
