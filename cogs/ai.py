import utils.sdapi as sdapi

import os
import io
import base64
import json
import typing

import discord
from discord.ext import commands
from discord import option

SD_ENDPOINT = os.getenv("SD_ENDPOINT")

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def sampler_autocomplete(self):
        samplers = []
        for sampler in sdapi.get_samplers(SD_ENDPOINT).json():
            samplers.append(sampler["name"])
        return samplers
    
    @staticmethod
    def model_autocomplete(self):
        models = []
        for model in sdapi.get_models(SD_ENDPOINT).json():
            models.append(model["title"])
        return models

    @staticmethod
    def style_autocomplete(self):
        styles = []
        for style in sdapi.get_styles(SD_ENDPOINT).json():
            styles.append(style["name"])
        return styles

    @commands.slash_command(name="sdprompt")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @option("prompt",           description="Prompt (what you want)")
    @option("negative_prompt",  description="Negative prompt (what you DONT want)", default="")
    @option("steps",            description="How many steps the model go through", default=26, max=128)
    @option("cfg_scale",        description="Classifier Free Guidance, defines how much the model should follow the text", default=12, max=36)
    @option("width",            default=512, max=1024)
    @option("height",           default=512, max=1024)
    @option("sampler",          autocomplete=sampler_autocomplete, default="Euler")
    @option("styles",           autocomplete=style_autocomplete, default="")
    @option("seed",             default=-1)
    async def sd_prompt(self, ctx: discord.ApplicationContext, prompt: str, negative_prompt: str, steps: int, cfg_scale: int, width: int, height: int, sampler: str, styles: str, seed: int):
        # omg so unprofeshunul 
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
        }

        r = await sdapi.txt2img_async(SD_ENDPOINT, prompt)
        if r["status"] != 200:
            raise commands.CommandInvokeError(f"Something went wrong - sdapi.txt2img returned {r['status']}")
        
        rjson = r["json"]

        for i in rjson["images"]:
            file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")

            embed = discord.Embed(
                description="Seed: " + str(json.loads(rjson["info"])["seed"]),
                color=discord.Color.random(seed=json.loads(rjson["info"])["seed"])
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.set_image(url="attachment://output.png")
            
            await ctx.send(file=file, embed=embed)

    @commands.slash_command(name="sdmodel")
    @commands.max_concurrency(1, commands.BucketType.guild)
    @option("model", autocomplete=model_autocomplete, description="Model you want")
    async def sd_model(self, ctx: discord.ApplicationCommand, model: str):
        payload = {
            "sd_model_checkpoint": model
        }
    
        await ctx.respond("Setting model", ephemeral=True)

        r = sdapi.set_settings(SD_ENDPOINT, payload)
        if r.status_code != 200:
            raise commands.CommandInvokeError(f"Something went wrong - sdapi.set_settings returned {r.status_code}")

        await ctx.respond("Set model")

    async def cog_command_error(self, ctx: discord.ApplicationContext, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("You're on cooldown", ephemeral=True)
        
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.respond("Max concurrency reached on command", ephemeral=True)
    
        if isinstance(error, commands.CommandInvokeError):
            await ctx.respond(error.original, ephemeral=True)

def setup(bot):
    bot.add_cog(AI(bot))