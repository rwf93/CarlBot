import os
import time

import discord
from discord.ext import commands

import asyncio
from cogwatch import Watcher

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

class CarlBot(discord.Bot):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print("Ready.")

    async def on_application_command_error(self, ctx: discord.ApplicationContext, exception: discord.DiscordException):
        if isinstance(exception, commands.CommandOnCooldown):
            await ctx.respond("You're on cooldown")

        if isinstance(exception, commands.MaxConcurrencyReached):
            await ctx.respond("Max concurrency reached on command")

        if isinstance(exception, commands.CommandInvokeError):
            await ctx.respond(exception.original)

async def main():
    bot = CarlBot()
    watcher = Watcher(bot, "cogs/", preload=True)
    await watcher.start()
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
