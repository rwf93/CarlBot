import utils.predicate as predicate
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name = "ping")
    async def ping(self, ctx):
        await ctx.respond("Ping!")

def setup(bot):
    bot.add_cog(Misc(bot))