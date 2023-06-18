import requests
import discord
from discord.ext import commands
import json
from typing import Union

from wow_helper import utils, config, db

logger = utils.get_logger(__name__)

RAIDER_IMG = 'https://cdnassets.raider.io/images/brand/Icon_FullColor_Square.png'
RAIDER_API = 'https://raider.io/api/v1/'
DEFAULT_REGION = 'us'


class RaiderIO(commands.Cog):
    """Commands relating to retrieving data from Raider IO"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Returns the current week\'s affixes', aliases=['affix'])
    async def affixes(self, ctx: commands.Context) -> None:
        guild_info = db.get_guild_information(ctx.guild.id)
        region = DEFAULT_REGION if guild_info[2] is None else guild_info[2]
        params = {
            'region': region,
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
    async def score(self, ctx: commands.Context, name: Union[str, None], *, realm: Union[str, None]) -> None:
        # TODO: Make this a callable function
        if name is None and realm is None:
            char_info = db.get_user_information(ctx.author.id)
        elif name is None or realm is None:
            logger.error('Improper usage of score command.')
            await ctx.send(f'Usage: {config.bot_prefix()}score CHARACTER REALM')
            return
        else:
            char_info = (name, realm, DEFAULT_REGION)

        if char_info is None:
            logger.error(f'Could not find information for user {ctx.author.id}.')
            await ctx.send('Be sure to use the command /set-character before executing this command with no arguments.')
            return

        char_info = (char_info[0].lower(), char_info[1].lower().replace(' ', '-'), char_info[2])

        params = {
            'region': char_info[2],
            'realm': char_info[1],
            'name': char_info[0],
            'fields': 'mythic_plus_scores_by_season:current'
        }
        logger.info(f'GET Request sent to {RAIDER_API}characters/profile')
        response = requests.get(RAIDER_API + 'characters/profile', params=params)
        if response.status_code != 200:
            logger.error('RaiderIO API is unresponsive.')
            await ctx.send('RaiderIO API is unresponsive.')
            return

        char_data = json.loads(response.text)

        embed = discord.Embed(title='RaiderIO Score')
        embed.set_thumbnail(url=char_data['thumbnail_url'])
        embed.add_field(name=char_data['name'], value=char_data['race'], inline=False)
        embed.add_field(name=char_data['class'], value=char_data['active_spec_name'], inline=False)
        embed.add_field(name='Score', value=char_data['mythic_plus_scores_by_season'][0]['scores']['all'], inline=False)
        await ctx.send(embed=embed)
