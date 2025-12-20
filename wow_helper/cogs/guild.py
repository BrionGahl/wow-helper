import asyncio

import discord
import requests
from discord.ext import commands

from wow_helper import utils, db, config

logger = utils.get_logger(__name__)

WOW_AUDIT_URL = 'https://wowaudit.com/v1/'
WOW_AUDIT_IMG = 'https://data.wowaudit.com/img/new-logo.svg'

HEADERS = {
            'Authorization': config.wow_audit_key()
}


class Guild(commands.Cog):
    """Commands relating to WoW guild assignment operations."""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description='Update WoW guild name.', aliases=['set-guild', 'guild-name', 'register-guild'])
    @commands.has_permissions(administrator=True)
    async def register_guild(self, ctx: commands.Context) -> None:
        logger.info(f'Updating WoW guild for Discord guild {ctx.guild.id}')
        reactions = {'🇺🇸': 'us', '🇪🇺': 'eu', '🇹🇼': 'tw', '🇰🇷': 'kr'}

        try:
            await ctx.message.author.send('Please enter your WoW guild name.')
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
        
        db.update_guild(ctx.guild.id, name=ctx.guild.name, wow_name=name.content, wow_server=server.content, wow_region=reactions[reaction.emoji])
        embed = discord.Embed(title='WoW Guild Set!')
        embed.add_field(name='Congrats!', value='With this set, you can now automatically query data for your guild!', inline=False)
        embed.add_field(name=f'{name.content}', value=f'{server.content}, {reactions[reaction.emoji].upper()}', inline=False)

        await ctx.message.author.send(embed=embed)
        await ctx.send(embed=embed)

        logger.info(f'Successfully updated guild data on guild {ctx.guild.id}.')

    @commands.command(description='Fetch upcoming scheduled raids.', aliases=['get-raids', 'raids'])
    async def get_raids(self, ctx: commands.Context) -> None:
        logger.info('Getting upcoming raids...')

        raids = self._get_raids()

        embed = discord.Embed(title="Upcoming Raids")
        embed.set_thumbnail(url=WOW_AUDIT_IMG)
        for raid in raids[0:6]:
            embed.add_field(name=f"{raid['difficulty']} {raid['instance']} on {raid['date']}",
                            value=f"From {raid['start_time']} to {raid['end_time']}",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(description='Fetch upcoming scheduled raid attendance.', aliases=['upcoming-absences'])
    @commands.has_permissions(administrator=True)
    async def check_attendance_for_upcoming_days(self, ctx: commands.Context, days: int = 2) -> None:
        raids = self._get_raids()

        ids: list[(int, str)] = []
        for i in range(days):
            ids.append((raids[i]['id'], raids[i]['date']))

        absences = {}
        for raid_id in ids:
            absences[raid_id[1]] = self._get_absences(raid_id[0])

        embed = discord.Embed(title="Upcoming Absences")
        embed.set_thumbnail(url=WOW_AUDIT_IMG)
        for key, value in absences.items():
            embed.add_field(name=f"Raid Day: {key}",
                            value=f"{','.join(value)}",
                            inline=False)
        await ctx.send(embed=embed)

    @staticmethod
    def _get_raids() -> list[dict]:
        logger.info(f'GET Request sent to {WOW_AUDIT_URL}raids?include_past=false')
        response = requests.get(WOW_AUDIT_URL + 'raids?include_past=false', headers=HEADERS)
        if response.status_code != 200:
            logger.error("WoWAudit is unresponsive.")
            return []

        raids = response.json()['raids']

        if len(raids) < 1:
            logger.error("No upcoming raids found.")
            return []

        return raids

    @staticmethod
    def _get_absences(raid_id: int) -> list[str]:
        output: list[str] = []
        logger.info(f'GET Request sent to {WOW_AUDIT_URL}raids/{raid_id}')
        response = requests.get(WOW_AUDIT_URL + f'raids/{raid_id}', headers=HEADERS)
        if response.status_code != 200:
            logger.error("WoWAudit is unresponsive.")
            return []

        signups = response.json()['signups']

        for signup in signups:
            if signup['status'] == 'Absent' or signup['status'] == 'Tentative':
                output.append(signup['character']['name'])

        return output
