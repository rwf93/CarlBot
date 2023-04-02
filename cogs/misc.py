from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"Pong!")

async def setup(client):
    await client.add_cog(Misc(client))