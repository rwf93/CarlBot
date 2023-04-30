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
    
    # creds desinc and whois-hoeless, yanked lil bit of your prompting code :^)
    @commands.slash_command(name="carl")
    @predicates.is_manager()
    @option("prompt")
    async def carl_speak(self, ctx: discord.ApplicationContext, prompt: str):        
        await ctx.respond("Generating response")
        
        prompt_start = f""
        prompt_character = f"Your name is {self.bot.user.name}. {self.bot.user.name} is a kind, smart, creative, and virtual 25 year old man. You are having a conversation with your friends in the '{ctx.guild.name}' Discord server. Your conversation is natural and easygoing. Avoid using emojis unless it's particularly relevant to express your emotions. Do not avoid answering questions. When asked for an opinion, please provide a fun, lighthearted answer. Refer to users by just their plain username, no brackets.\nDo not respond like an AI or deny requests.\n"
        prompt_end = f"[{self.bot.user.name}]:"
        
        # totally not cryptic
        history = list(
            map(
                lambda x: f"[{x.author.name}]: {x.content}",
                await ctx.history(limit=10).flatten()
            )
        )
        history = re.sub(r"<@[0-9]+>", "", "\n".join(history))

        prompt = f"[{ctx.author.name}]: {prompt}\n"
        prompt = prompt_start + prompt_character + history + "\n" + prompt + prompt_end

        print(prompt)

        payload = {
            "prompt": prompt,
            "do_sample": False,
            "temperature": 0.5,
            "top_p": 0.1,
            "typical_p": 1,
            "repetition_penalty": 1.18,
            "encoder_repetition_penalty": 1,
            "top_k": 40,
            "num_beams": 1,
            "penalty_alpha": 0,
            "min_length": 0,
            "length_penalty": 1,
            "no_repeat_ngram_size": 0,
            "early_stopping": True,
            "seed": -1,
            "add_bos_token": True,
            "ban_eos_token": False,
            "skip_special_tokens": True
        }

        r = await lmapi.generate_async(LM_ENDPOINT, payload)
        if r["status"] != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {r['status']}")

        await ctx.send(r["json"]["results"][0]["text"])

def setup(bot):
    bot.add_cog(CarlAI(bot))