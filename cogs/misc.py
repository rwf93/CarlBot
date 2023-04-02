from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command()
    async def ping(self, ctx):
        await ctx.respond("Pong!")

def setup(bot):
    bot.add_cog(Misc(bot))