import os
import time

from discord.ext import commands
import discord

from utils.watchdog import setup_watchdog, kill_watchdog

from dotenv import load_dotenv
load_dotenv()

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    print(f'Registering cog: {filename[:-3]}')
    bot.load_extension(f'cogs.{filename[:-3]}')

# WATCH_DOGS HIT VDIEO GAME????????
def watch_cogs(src): 
   filename = os.path.basename(src)
   if filename.endswith('.py'):
      print(f'Reloading cog: {filename[:-3]}')
      bot.reload_extension(f'cogs.{filename[:-3]}')

cog_watcher = setup_watchdog(watch_cogs, "cogs/")

bot.run(os.getenv("BOT_TOKEN"))

kill_watchdog(cog_watcher)