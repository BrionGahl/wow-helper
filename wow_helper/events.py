import discord
from discord.ext import commands

from wow_helper import db


def setup(bot: commands.Bot) -> None:
    message_send_event(bot)
    guild_join_event(bot)


def guild_join_event(bot: commands.Bot):
    @bot.event
    async def on_guild_join(ctx: discord.Guild):
        db.insert_guild(ctx.id, ctx.name)


def message_send_event(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message) -> None:
        await bot.process_commands(message)