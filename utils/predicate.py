import os
import discord
from discord.ext import commands

def is_owner():
    async def predicate(ctx: discord.ApplicationContext):
        return ctx.author.id == int(os.getenv("BOT_OWNER"))
    return commands.check(predicate)

# this is pure evil
def is_admin():
    async def predicate(ctx: discord.ApplicationContext):
        admin_roles = list(map(
            lambda x: int(x),
            os.getenv("BOT_ADMIN_ROLES").split(",")
        ))
        snowflake_roles = list(map(
            lambda x: x.id,
            ctx.author.roles
        ))
        return any(x in admin_roles for x in snowflake_roles)
    return commands.check(predicate)