from wow_helper.cogs.raider_io import *
from wow_helper.cogs.guild import *


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RaiderIO(bot))
    await bot.add_cog(Guild(bot))
