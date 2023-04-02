import utils.sdapi as sdapi

import os
import io
import base64

import discord
from discord.ext import commands
from discord import option

samplers = []
models = []

for sampler in sdapi.get_samplers(os.getenv('SD_ENDPOINT')).json():
    samplers.append(sampler["name"])

for model in sdapi.get_models(os.getenv('SD_ENDPOINT')).json():
    models.append(sampler["title"])

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="sdprompt")
    
    @option("prompt", description="Prompt (what you want)")
    @option("width", default=512, max=1024)
    @option("height", default=512, max=1024)
    # DEFAULTS HAVE TO BE FUCKING LAST FOR SOME FUCKING REASON
    @option("steps", description="How many steps the model go through", default=26, max=128)
    @option("cfg_scale", description="Classifier Free Guidance", default=12, max=36)
    @option("negative_prompt", description="Negative prompt (what you DONT want)", default="")
    @option("sampler", choices=samplers, default="Euler")
    async def sd_prompt(self, ctx: discord.ApplicationContext, prompt: str, negative_prompt: str, steps: int, cfg_scale: int, sampler: str, width: int, height: int):
        await ctx.respond("Please wait while we generate your ~~porn~~ image")
        
        prompt = {
            "prompt":           prompt,
            "negative_prompt":  negative_prompt,
            
            "steps":            steps,
            "cfg_scale":        cfg_scale,
            
            "width":            width,
            "height":           height,

            "sampler_index":    sampler
        }

        r = sdapi.txt2img(os.getenv("SD_ENDPOINT"), prompt).json()

        for i in r["images"]:
            file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")
            await ctx.respond(file=file)

def setup(bot):
    bot.add_cog(AI(bot))