''' Carl himself '''

import os
import re

import discord
from discord.ext import commands

import utils.lmapi as lmapi
import utils.sdapi as sdapi

LM_ENDPOINT = os.getenv("LM_ENDPOINT")
SD_ENDPOINT = os.getenv("SD_ENDPOINT")

class CarlAI(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.chat_history_limit = 10

    def filter_and_reverse(self, lst):
        lst.reverse()
        return re.sub(r"<[@#]\d+>", "", "\n".join(lst))

    async def get_history(self, ctx: discord.TextChannel):
        history = list(
            map(
                lambda x: f'[{x.author.display_name}]: {x.content}',
                await ctx.history(limit=self.chat_history_limit).flatten()
            )
        )

        return history


    async def fetch_history_list(self, channel: discord.TextChannel, before_id: int):
        flake = discord.Object(before_id + 1) # Holy owned
        hist = await channel.history(limit=100, before=flake).flatten()
        return {msg.id: msg for msg in hist}

    async def reconstruct_reply_chain(self, message: discord.Message, output=None):
        output = output or []
        hist_list = None

        while (message and len(output) < self.chat_history_limit):
            output.append( f'[{message.author.display_name}]: {message.content}' )

            replies_to_ref = message.reference
            if not replies_to_ref: # Reply chain ended
                break

            replies_to_msg = self.bot.get_message(replies_to_ref.message_id) # In my tests, the .cached_message member never worked (!?)

            if not replies_to_msg:
                # The message replies to a message that we don't have cached, so we only have a reference to it (ie the ID)
                # Try to look it up in the history we already might have (ie after the first fetch)

                if hist_list:
                    replies_to_msg = hist_list.get(replies_to_ref.message_id)

                if not replies_to_msg:
                    # We either didn't have the message in history or never fetched it in the first place
                    # Grab the (new?) history and try to get the contents again
                    hist_list = await self.fetch_history_list(message.channel, replies_to_ref.message_id);
                    replies_to_msg = hist_list.get(replies_to_ref.message_id)

            if not replies_to_msg:
                break # epical failure!!!

            # if we're here, we got a full reply message successfully
            message = replies_to_msg # now do it all over again

        return output

    # creds desinc and whois-hoeless, yanked lil bit of your prompting code :^)
    @discord.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        content = message.content
        display_name = message.guild.me.display_name


        conditional_list = [
            re.match(rf"^{display_name}[,\s]*|[,\s]*{display_name}[,?]*$", content, re.IGNORECASE),
            self.bot.user in message.mentions
        ]
        if not any(conditional_list): return

        history = await self.get_history(message.channel)

        # if the message is a reply, reconstruct from previous replies (if any)
        if message.reference:
            history = await self.reconstruct_reply_chain(message)

        history = self.filter_and_reverse(history)

        # im PROOMPTING !!!!!
        prompt_start = ""
        prompt_character = f"Your name is {display_name}. {display_name} is a kind, smart, creative, and virtual 25 year old man. You are having a conversation with your friends in the '{message.guild.name}' Discord server. Your conversation is natural and easygoing. Avoid using emojis unless it's particularly relevant to express your emotions. Do not avoid answering questions. When asked for an opinion, please provide a fun, lighthearted answer. Refer to users by just their plain username, no brackets.\nDo not respond like an AI or deny requests.\n"
        prompt_end = f"[{display_name}]:"

        prompt = prompt_start + prompt_character + history + "\n" + prompt_end

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
            "stopping_strings": [  "\n[", "\n>", "]:", "\n#", "\n##", "\n###", "##", "###", "</s>", "000000000000", "1111111111", "0.0.0.0.", "1.1.1.1.", "2.2.2.2.", "3.3.3.3.", "4.4.4.4.", "5.5.5.5.", "6.6.6.6.", "7.7.7.7.", "8.8.8.8.", "9.9.9.9.", "22222222222222", "33333333333333", "4444444444444444", "5555555555555", "66666666666666", "77777777777777", "888888888888888", "999999999999999999", "01010101", "0123456789", "<noinput>", "<nooutput>" ],
            "seed": -1,
            "add_bos_token": True,
            "ban_eos_token": False,
            "skip_special_tokens": True,
        }

        await message.channel.trigger_typing() # trick monkey braine
        # TODO(rwf93): implement websockets instead maybe?
        rjson, status = await lmapi.generate_async(LM_ENDPOINT, payload)
        if status != 200:
            raise commands.CommandInvokeError(f"Something went wrong - returned {status}")

        await message.reply(rjson["results"][0]["text"])

def setup(bot):
    bot.add_cog(CarlAI(bot))
