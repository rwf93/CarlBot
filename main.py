import discord
import os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    print(f'Registering cog: {filename[:-3]}')
    bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("BOT_TOKEN"))
