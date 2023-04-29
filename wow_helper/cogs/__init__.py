from discord.ext import commands

from wow_helper.cogs.raider_io import RaiderIO
from wow_helper.cogs.guild import Guild
from wow_helper.cogs.user import User


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RaiderIO(bot))
    await bot.add_cog(Guild(bot))
    await bot.add_cog(User(bot))
