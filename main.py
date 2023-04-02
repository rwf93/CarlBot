import discord
import os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

class CarlBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = os.getenv("BOT_PREFIX"),
            intents = intents
        )

    async def setup_hook(self): 
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                print(f"Registering cog: {filename[:-3]}")
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()

client = CarlBot()
client.run(os.getenv("BOT_TOKEN"))
