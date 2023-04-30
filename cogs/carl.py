import utils.lmapi as lmapi
import utils.sdapi as sdapi

import utils.predicate as predicates

import os
import re
import io
import base64

import discord
from discord.ext import commands, tasks
from discord import option

LM_ENDPOINT = os.getenv("LM_ENDPOINT")
SD_ENDPOINT = os.getenv("SD_ENDPOINT")

class CarlAI(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    async def generate_selfie(self, ctx, prompt): 
        prompt_start = f"After describing the image he took, {self.bot.user.name} may reply.\n"
        prompt_end = "Nouns of things in the photo separated by a comma: "
        
        full_prompt = prompt_start + prompt + prompt_end

        payload = {
            "prompt": full_prompt,
            "max_new_tokens": 200,
        }

        r = lmapi.generate(LM_ENDPOINT, payload)
        if r.status_code != 200:
            raise commands.CommandInvokeError(f"Something went wrong - lmapi.generate returned {r.status_code}")

        lm_prompt = r.json()["results"][0]["text"]
        
        positive_prompt = "masterpiece, best quality, 25 yearold man," + lm_prompt
        negative_prompt = "EasyNegative, bad-hands-5"

        prompt = {
            "prompt":           positive_prompt,
            "negative_prompt":  negative_prompt,
            
            "steps":            36,
            "cfg_scale":        12,
            
            "width":            512,
            "height":           512,
        }
        
        r = sdapi.txt2img(SD_ENDPOINT, prompt)
        if r.status_code != 200:
            raise commands.CommandInvokeError(f"Something went wrong - sdapi.txt2img returned {r.status_code}")

        rjson = r.json()

        for idx, i in enumerate(rjson["images"]):
             file = discord.File(io.BytesIO(base64.b64decode(i.split(",",1)[0])), filename="output.png")
             await ctx.send(file=file)

    @commands.slash_command(name="carl")
    @predicates.is_manager()
    @option("prompt")
    async def carl_speak(self, ctx: discord.ApplicationContext, prompt: str):
        prompt_start = "\n### Instruction:\nWrite a reply to the last message as if it was a chatroom.\n### Input:\n"
        prompt_end = f"### Response:\n{self.bot.user.name} said: \n"

        history = list(
            map(
                lambda x: f"{x.author.name} said: {x.content}",
                filter(
                    lambda y: (y.author.id != self.bot.application_id),
                    await ctx.history(limit=25).flatten()
                )
            )
        )
        history = "\n".join(history)

        real_prompt = f"{ctx.author.name} said: {prompt}\n"
        full_prompt = prompt_start + history + "\n" + real_prompt + prompt_end

        print(full_prompt)

        payload = {
            "prompt": full_prompt,
            "max_new_tokens": 250,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.1,
            "typical_p": 1,
            "repetition_penalty": 1.18,
            "encoder_repetition_penalty": 1,
            "top_k": 40,
            "no_repeat_ngram_size": 0,
            "num_beams": 1,
            "penalty_alpha": 0,
            "length_penalty": 1,
            "early_stopping": False,
            "add_bos_token": True,
        }

        await ctx.respond("Generating response")

        # TODO(rwf93): make less garbage...
        if "selfie" in prompt:
            await self.generate_selfie(ctx, re.sub(r"^.*?selfie", "selfie", prompt))
            return

        r = lmapi.generate(LM_ENDPOINT, payload)
        if r.status_code != 200:
            raise commands.CommandInvokeError(f"Something went wrong - lmapi.generate returned {r.status_code}")

        await ctx.send(r.json()["results"][0]["text"])

def setup(bot):
    bot.add_cog(CarlAI(bot))