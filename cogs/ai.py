import utils.sdapi as sdapi
import utils.predicate as predicates
import utils.autocomplete as autocomplete

import os
import io
import base64
import json
import typing
import requests

import discord.utils as discordutils
import discord
from discord.ext import commands, tasks
from discord import option

SD_ENDPOINT = os.getenv("SD_ENDPOINT")

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invalidate_sdcache.start()

    @staticmethod
    def samplers_autocomplete(self, ctx):
        samplers = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i['name'],
            self.sampler_json
        ))

        return samplers
    
    @staticmethod
    def models_autocomplete(self, ctx):
        models = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i['title'],
            self.models_json
        ))
        
        return models

    @staticmethod
    def styles_autocomplete(self, ctx):
        styles = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i['name'],
            self.styles_json
        ))

        return styles
    
    @staticmethod
    def upscalers_autocomplete(self, ctx):
        upscalers = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i['name'],
            self.upscalers_json
        ))

        return upscalers

    @tasks.loop(seconds=30)
    async def invalidate_sdcache(self):
        self.sampler_json   = sdapi.get_samplers(SD_ENDPOINT).json()
        self.models_json    = sdapi.get_models(SD_ENDPOINT).json()
        self.styles_json    = sdapi.get_styles(SD_ENDPOINT).json()
        self.upscalers_json = sdapi.get_upscalers(SD_ENDPOINT).json()
    
    @commands.slash_command(name="sdprompt")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @option("prompt",           description="Prompt (what you want)")
    @option("negative_prompt",  description="Negative prompt (what you DONT want)", default="")
    @option("steps",            description="How many steps the model go through", default=26, max=128)
    @option("cfg_scale",        description="Classifier Free Guidance, defines how much the model should follow the text", default=12, max=36)
    @option("width",            default=512, max=1024)
    @option("height",           default=512, max=1024)
    @option("sampler",          autocomplete=samplers_autocomplete, default="Euler a")
    @option("styles",           autocomplete=styles_autocomplete, default="")
    @option("seed",             default=-1)
    async def sd_prompt(self, ctx: discord.ApplicationContext, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str, styles: str, seed: int):
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
    @option("model", autocomplete=models_autocomplete, description="Model you want")
    @predicates.is_admin()
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
    
    @commands.slash_command(name="sdupscale")
    @option("upscaler_one",       autocomplete=upscalers_autocomplete)
    @option("upscaler_two",       autocomplete=upscalers_autocomplete, default="None")
    @option("upscaler_amt",       default=2, max=4)
    @predicates.is_admin()
    async def sd_upscale(self, ctx: discord.ApplicationContext, file: discord.Attachment, upscaler_one: str, upscaler_two: str, upscaler_amt: float):
        await ctx.respond("Upscaling image")
        
        b64_image = 'data:image/png;base64,' + base64.b64encode(requests.get(file.url, stream=True).content).decode('utf-8')
        
        payload = {
            "upscaler_1":       upscaler_one,
            "upscaler_2":       upscaler_two,
            "upscaling_resize": upscaler_amt,
            "image":            b64_image
        }

        r = await sdapi.upscale_single_async(SD_ENDPOINT, payload)
        if r["status"] != 200:
            raise commands.CommandInvokeError(f"Something went wrong - upscale_single returned {r['status']}")
        
        file = discord.File(io.BytesIO(base64.b64decode(r["json"]["image"])), filename="output.png")

        await ctx.respond(file=file)

def setup(bot):
    bot.add_cog(AI(bot))