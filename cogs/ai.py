import utils.sdapi as sdapi

import os
import io
import base64
import json

import discord
from discord.ext import commands
from discord import option

SD_ENDPOINT=os.getenv("SD_ENDPOINT")

samplers = []
styles = []
models = []
upscalers = []

for sampler in sdapi.get_samplers(SD_ENDPOINT).json():
    samplers.append(sampler["name"])

for model in sdapi.get_models(SD_ENDPOINT).json():
    models.append(model["model_name"])

for style in sdapi.get_styles(SD_ENDPOINT).json():
    styles.append(style["name"])

for upscaler in sdapi.get_upscalers(SD_ENDPOINT).json():
    upscalers.append(upscaler["model_name"])

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="sdprompt")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @option("prompt",           description="Prompt (what you want)")
    @option("negative_prompt",  description="Negative prompt (what you DONT want)", default="")
    @option("steps",            description="How many steps the model go through", default=26, max=128)
    @option("cfg_scale",        description="Classifier Free Guidance", default=12, max=36)
    @option("width",            default=512, max=1024)
    @option("height",           default=512, max=1024)
    @option("sampler",          choices=samplers, default="Euler")
    @option("styles",           choices=styles, default="")
    @option("seed",             default=-1)
    @option("upscaler",         choices=upscalers, default = "")
    @option("upscaler_scale",   default=2, max=4)
    async def sd_prompt(self, ctx: discord.ApplicationContext, prompt: str, negative_prompt: str, steps: int, cfg_scale: int, width: int, height: int, sampler: str, styles: str, seed: int, upscaler: str, upscaler_scale: int):
        await ctx.respond("Please wait while we generate your ~~porn~~ image")
        
        prompt = {
            "prompt":           prompt,
            "negative_prompt":  negative_prompt,
            
            "steps":            steps,
            "cfg_scale":        cfg_scale,
            
            "width":            width,
            "height":           height,

            "sampler_index":    sampler,
            
            "styles":           [ styles ],
            # sneed
            "seed":             seed,

            "hr_upscaler":      upscaler,
            "hr_scale":         upscaler_scale
        }

        r = sdapi.txt2img(os.getenv("SD_ENDPOINT"), prompt).json()

        for i in r["images"]:
            file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")

            embed = discord.Embed(
                description="Seed: " + str(json.loads(r["info"])["seed"]),
                color=discord.Color.random(seed=json.loads(r["info"])["seed"])
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.set_image(url="attachment://output.png")
            
            await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(AI(bot))