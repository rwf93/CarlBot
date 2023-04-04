import os
import discord
from discord.ext import commands

def is_owner():
    async def predicate(ctx: discord.ApplicationContext):
        return ctx.author.id == int(os.getenv("BOT_OWNER"))
    return commands.check(predicate)