import os
import time

from discord.ext import commands
import discord

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
        
async def main():
    bot = CarlBot()
    watcher = Watcher(bot, "cogs/", preload=True)
    await watcher.start()
    await bot.start(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())