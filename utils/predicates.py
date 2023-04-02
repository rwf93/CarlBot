import os
from discord.ext import commands

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == os.getenv("BOT_OWNER") 
    return commands.check(predicate)

def is_in_guild(gid):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == gid
    return commands.check(predicate)