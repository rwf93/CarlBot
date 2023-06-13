from main import CarlBot

import utils.predicate as predicate
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot: CarlBot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name = "ping")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! ({round(self.bot.latency * 1000, 1)}ms)")

def setup(bot):
    bot.add_cog(Misc(bot))
