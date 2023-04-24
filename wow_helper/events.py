import discord
from discord.ext import commands

from wow_helper import db


def setup(bot: commands.Bot) -> None:
    message_send_event(bot)
    guild_join_event(bot)
    guild_remove_event(bot)
    guild_update_event(bot)


def guild_join_event(bot: commands.Bot):
    @bot.event
    async def on_guild_join(guild: discord.Guild):
        db.insert_guild(guild.id, guild.name)


def guild_remove_event(bot: commands.Bot):
    @bot.event
    async def on_guild_remove(guild: discord.Guild):
        db.delete_guild(guild.id)


def guild_update_event(bot: commands.Bot):
    @bot.event
    async def on_guild_update(old_guild: discord.Guild, new_guild: discord.Guild):
        db.update_guild(old_guild.id, name=new_guild.name)


def message_send_event(bot: commands.Bot) -> None:
    @bot.event
    async def on_message(message) -> None:
        await bot.process_commands(message)
