import utils.lmapi as lmapi
import utils.predicate as predicates

import os

import discord
from discord.ext import commands, tasks
from discord import option

LM_ENDPOINT = os.getenv("LM_ENDPOINT")

class CarlAI(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(name="carl")
    @predicates.is_manager()
    @option("prompt")
    async def carl_speak(self, ctx: discord.ApplicationContext, prompt: str):
        prompt_start = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n### Instruction:\nWrite a reply to the last message.\n### Input:\n"
        prompt_end = f"### Response:\n"

        # sorta bigbrain maybe?
        history = "\n".join(
            list(
                map(
                    lambda x: f'{x.author.name} said: {x.content}',
                    filter(
                        lambda y: (y.author.id != self.bot.application_id) and y.type != discord.MessageType.application_command, 
                        await ctx.history(limit=25).flatten()
                    )
                )
            )
        )
        real_prompt = f'[{ctx.author.name}]: {prompt}\n'
        full_prompt = prompt_start + history + "\n" + real_prompt + prompt_end

        print(full_prompt)

        payload = {
            'prompt': full_prompt,
            'max_new_tokens': 250,
        }

        await ctx.respond("Generating response")
        
        r = lmapi.generate(LM_ENDPOINT, payload)
        if r.status_code != 200:
            raise commands.CommandInvokeError(f"Something went wrong - lmapi.generate returned {r.status_code}")

        await ctx.send(r.json()['results'][0]['text'])

def setup(bot):
    bot.add_cog(CarlAI(bot))