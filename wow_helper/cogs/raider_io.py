import requests
import discord

import json
from discord.ext import commands

from wow_helper import utils
from wow_helper import config

logger = utils.get_logger(__name__)

RAIDER_IMG = 'https://cdnassets.raider.io/images/brand/Icon_FullColor_Square.png'
RAIDER_API = 'https://raider.io/api/v1/'


class RaiderIO(commands.Cog):
    """Commands relating to retrieving data from Raider IO"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Returns the current week\'s affixes', aliases=['affix'])
    async def affixes(self, ctx: commands.Context) -> None:
        params = {
            'region': 'us',
            'locale': 'en'
        }
        logger.info(f'GET Request sent to {RAIDER_API}mythic-plus/affixes')
        response = requests.get(RAIDER_API + 'mythic-plus/affixes', params=params)
        if response.status_code != 200:
            logger.error('RaiderIO API is unresponsive.')
            await ctx.send('RaiderIO API is unresponsive')
            return

        affix_data = response.json()['affix_details']

        embed = discord.Embed(title='This Week\'s Affixes')
        embed.set_thumbnail(url=RAIDER_IMG)
        for affix in affix_data:
            embed.add_field(name=affix['name'], value=affix['description'], inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['raiderscore', 'io'])
    async def score(self, ctx: commands.Context, name: str, realm: str):
        # More work to make it have char portrait
        params = {
            'region': 'us',
            'realm': realm,
            'name': name,
            'fields': 'mythic_plus_scores_by_season:current'
        }
        logger.info(f'GET Request sent to {RAIDER_API}characters/profile')
        response = requests.get(RAIDER_API + 'characters/profile', params=params)
        if response.status_code != 200:
            logger.error('RaiderIO API is unresponsive.')
            await ctx.send('RaiderIO API is unresponsive')
            return

        char_data = json.loads(response.text)

        embed = discord.Embed(title='RaiderIO Score')
        embed.set_thumbnail(url=char_data['thumbnail_url'])
        embed.add_field(name=char_data['name'], value=char_data['race'], inline=False)
        embed.add_field(name=char_data['class'], value=char_data['active_spec_name'], inline=False)
        embed.add_field(name='Score', value=char_data['mythic_plus_scores_by_season'][0]['scores']['all'], inline=False)
        await ctx.send(embed=embed)

    @score.error
    async def score_error(self, ctx: commands.Context, error: commands.CommandError):
        logger.error(f'{error}')
        await ctx.send(f'Usage: {config.bot_prefix()}score [CHARACTER] [REALM]')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RaiderIO(bot))
