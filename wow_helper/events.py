import discord
from discord.ext import commands


def setup(bot: commands.Bot) -> None:
    message_send(bot)


def message_send(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message) -> None:
        await bot.process_commands(message)