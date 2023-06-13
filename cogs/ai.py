""" A raw method of interacting with SDAPI and LMAPI """

import os
import io
import base64
import json
import re
import requests

from main import CarlBot

import discord
from discord.ext import commands, tasks
from discord import option

import utils.sdapi as sdapi
import utils.lmapi as lmapi

import utils.predicate as predicates
import utils.autocomplete as autocomplete

SD_ENDPOINT = os.getenv("SD_ENDPOINT")
LM_ENDPOINT = os.getenv("LM_ENDPOINT")

class AI(commands.Cog):
    def __init__(self, bot: CarlBot):
        self.bot = bot
        self.invalidate_sdcache.start()

    def samplers_autocomplete(self, ctx):
        samplers = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i["name"],
            self.sampler_json
        ))

        return samplers

    def models_autocomplete(self, ctx):
        models = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i["title"],
            self.models_json
        ))

        return models

    def styles_autocomplete(self, ctx):
        styles = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i["name"],
            self.styles_json
        ))

        return styles

    def upscalers_autocomplete(self, ctx):
        upscalers = autocomplete.basic_autocomplete(ctx, map(
            lambda i: i["name"],
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
    @option("clip_skip",        default=2, max=4)
    async def sd_prompt(self, ctx: discord.ApplicationContext, prompt: str, negative_prompt: str, steps: int, cfg_scale: float, width: int, height: int, sampler: str, styles: str, seed: int, clip_skip: int):
        # sneaky beaky
        await ctx.respond("Please wait while we generate your ~~\x70\x6f\x72\x6e~~ image")

        payload = {
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

            "clip_skip": clip_skip
        }

        rjson, status = await sdapi.txt2img_async(SD_ENDPOINT, payload)
        if status != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {status}")

        info = json.loads(rjson["info"])

        for idx, i in enumerate(rjson["images"]):
            file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")

            info_model = re.search("Model: ([^,]+)", info["infotexts"][idx]).group(1)
            info_seed = info["seed"]

            embed = discord.Embed(
                color=discord.Color.random(seed=info_seed)
            )

            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.set_image(url="attachment://output.png")

            embed.add_field(name="Seed", value=f"{info_seed}")
            embed.add_field(name="Model", value=info_model)

            await ctx.send(file=file, embed=embed)

    @commands.slash_command(name="sdmodel")
    @commands.max_concurrency(1, commands.BucketType.guild)
    @option("model", autocomplete=models_autocomplete, description="Model you want")
    @predicates.is_manager()
    async def sd_model(self, ctx: discord.ApplicationCommand, model: str):
        payload = {
            "sd_model_checkpoint": model
        }

        await ctx.respond("Setting model")

        _, status = await sdapi.set_settings_async(SD_ENDPOINT, payload)
        if status != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {status}")

        await ctx.respond(f"Set model to: {model}")

    @commands.slash_command(name="sdupscale")
    @option("upscaler_one",       autocomplete=upscalers_autocomplete)
    @option("upscaler_two",       autocomplete=upscalers_autocomplete, default="None")
    @option("upscaler_amt",       default=2, max=4)
    @predicates.is_manager()
    async def sd_upscale(self, ctx: discord.ApplicationContext, file: discord.Attachment, upscaler_one: str, upscaler_two: str, upscaler_amt: float):
        await ctx.respond("Upscaling image")

        b64_image = "data:image/png;base64," + base64.b64encode(requests.get(file.url, stream=True).content).decode("utf-8")

        payload = {
            "upscaler_1":       upscaler_one,
            "upscaler_2":       upscaler_two,
            "upscaling_resize": upscaler_amt,
            "image":            b64_image
        }

        rjson, status = await sdapi.upscale_single_async(SD_ENDPOINT, payload)
        if status != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {status}")

        file = discord.File(io.BytesIO(base64.b64decode(rjson["image"])), filename="output.png")

        await ctx.respond(file=file)

    @commands.slash_command(name="lmprompt")
    @predicates.is_manager()
    @option("prompt")
    async def lm_prompt(self, ctx: discord.ApplicationCommand, prompt: str):
        payload = {
            "prompt": prompt,
            "max_new_tokens": 250,
        }

        await ctx.respond("Generating LM output")

        rjson, status = await lmapi.generate_async(LM_ENDPOINT, payload)
        if status != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {status}")

        await ctx.send(rjson["results"][0]["text"])

def setup(bot):
    bot.add_cog(AI(bot))
