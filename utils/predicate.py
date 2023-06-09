import os
import discord
from discord.ext import commands

def is_owner():
    async def predicate(ctx: discord.ApplicationContext):
        return ctx.author.id == int(os.getenv("BOT_OWNER"))
    return commands.check(predicate)

# checks if author is owner OR has an manager role
def is_manager():
    async def predicate(ctx: discord.ApplicationContext):
        if ctx.author.id == int(os.getenv("BOT_OWNER")): return True
        admin_roles     = [int(x) for x in os.getenv("BOT_MANAGER_ROLES").split(",")]
        snowflake_roles = [x.id for x in ctx.author.roles]
        return any(x in admin_roles for x in snowflake_roles)
    return commands.check(predicate)
