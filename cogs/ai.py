import utils.sdapi as sdapi
import os
import io
import base64

import discord
from discord.ext import commands

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    class PromptFlags(commands.FlagConverter):
        prompt:          str = commands.flag(description="Main prompt (what you want)")
        negative_prompt: str = commands.flag(default="nsfw", description="Negative prompt (what you DONT want)")
        
        steps:           int = commands.flag(default=26, description="Amount of steps it will pass through the model")
        cfg_scale:       int = commands.flag(default=12, description="classifier free guidance, defines how much the image generation process follows the text prompt")
        
        width:           int = commands.flag(default=512)
        height:          int = commands.flag(default=512)

        sampler_index:   str = commands.flag(default="Euler", description="What sampler to use (use /sdsamplers)")

    @commands.hybrid_command(name="sdprompt")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sd_prompt(self, ctx, *, flags: PromptFlags):
        await ctx.reply("Please wait you dipfuck")
        
        prompt = {
            "prompt": flags.prompt,
            "negative_prompt": flags.negative_prompt,
            
            "steps": flags.steps,
            "cfg_scale": flags.cfg_scale,
            
            "width": flags.width,
            "height": flags.height,

            "sampler_index": flags.sampler_index
        }
        
        r = sdapi.txt2img(os.getenv("SD_ENDPOINT"), prompt).json()
    
        for i in r["images"]:
            file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")
            await ctx.reply(file=file)

    @commands.hybrid_command(name="sdmodels")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sd_models(self, ctx):
        r = sdapi.get_models(os.getenv("SD_ENDPOINT")).json()
        reply = "Available models: ```"
        for i in r:
            reply = reply + f'{i["title"]}\n'
        reply = reply + "```"

        await ctx.reply(reply)

    @commands.hybrid_command(name="sdsamplers")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sd_samplers(self, ctx):
        r = sdapi.get_samplers(os.getenv("SD_ENDPOINT")).json()
        reply = "Available samplers: ```"
        for i in r:
            reply = reply + f'{i["name"]}\n'
        reply = reply + "```"

        await ctx.reply(reply)
    
async def setup(client):
    await client.add_cog(AI(client))