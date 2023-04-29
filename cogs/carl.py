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
        prompt_start = "### Instruction:\r\nWrite the next message in this Discord chat room.\r\n"
        prompt_end = f"### Reply to this user.\r\n[{self.bot.user.display_name}]: "

        # sorta bigbrain maybe?
        history = "\r\n".join(
            list(
                map(
                    lambda x: f'[{x.author.name}]: {x.content}',
                    filter(
                        lambda y: (y.author.id != self.bot.application_id) and y.type != discord.MessageType.application_command, 
                        await ctx.history(limit=25).flatten()
                    )
                )
            )
        )
        real_prompt = f'[{ctx.author.name}]: {prompt}\r\n'
        full_prompt = prompt_start + history + "\r\n" + real_prompt + prompt_end

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