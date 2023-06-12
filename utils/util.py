import re
import discord
from fuzzywuzzy import process

def basic_autocomplete(ctx, items):
    return list(
        filter(
            lambda x: x.lower().startswith(ctx.value.lower()),
            items
        )
    )

def fuzzy_autocomplete(ctx, items):
    return list(
        map(
            lambda x: x[0],
            process.extract(ctx.value.lower(), items)
        )
    )

async def get_history(ctx: discord.ApplicationContext | discord.TextChannel, lim: int):
    history = list(
        map(
            lambda x: f"[{x.author.name}]: {x.content}",
            await ctx.history(limit=lim).flatten()
        )
    )

    return re.sub(r"<@[0-9]+>", "", "\n".join(history))