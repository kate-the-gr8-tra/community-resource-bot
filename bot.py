import discord
from discord.ext import commands
import logging
import discord.ext.commands.bot
from emoji_list import EmojiList
import asyncio

intents = discord.Intents.default()
emoji_list = EmojiList()

#~~~ TESTING SECTION ~~~
with open('info.txt', "r") as file:
    GUILD_IDS = file.read().splitlines()[0]
    BOT_TOKEN = file.read().splitlines()[1]
#~~~ TESTING SECTION ~~~


class ResourceBot(commands.Bot):
    def __init__(self, bot):
        super().__init__(command_prefix = '!', intents = intents)
        self.bot = bot
        self.__hourly_phrase_toggle = False #will be for toggling the hourly phrase in a later function

    async def setup_hook(self):
        print("Setting up...")
        try:
            self.tree.clear_commands(guild=discord.Object(id=GUILD_IDS))
            self.tree.copy_global_to(guild=discord.Object(id = GUILD_IDS))
            await self.tree.sync(guild=discord.Object(id = GUILD_IDS))  
            print("Commands synced") 
        except Exception as e:
            print(f"Error during command sync: {e}")

    async def on_ready(self):
        print(f"'Logged in as {self.user}!'") 

    # Override on_message event
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return #do nothing if message came from a bot
        
        cop_trigger_phrases = ["cop", "cops", "pigs", "pig", "police", "acab"]
        heat_from_fire = "heat from fire"
        nazi_trigger_phrases = ["nazi", "nazis" "fascist", "fascists" "fascism"]
        nazi_german_trigger = "nationalsozialistisch"

        for cop_phrase in cop_trigger_phrases:
            if cop_phrase in [word for word in message.content.split(" ").lower()]:
                await message.channel.send(f"ACAB! {emoji_list.get(":police_officer:")} 
                {emoji_list.get(":heavy_equals_sign:")} {emoji_list.get(":pig:")}")

        if heat_from_fire in [word for word in message.content.split(" ").lower()]:
            await message.channel.send("Heat from fire! :3")

        for nazi_phrase in nazi_trigger_phrases:
            if nazi_phrase in [word for word in message.content.split(" ").lower()]:
                await message.channel.send(f"MAKE THE WORLD A BETTER PLACE PUNCH A NAZI IN THE FACE! {emoji_list.get(":punch:")}")

        if nazi_german_trigger in [word for word in message.content.split(" ").lower()]:
            await message.channel.send(f"MACH DIE WELT EINEN BESSEREN ORT, SCHLAG EINEM NAZI INS GESICHT! {emoji_list.get(":punch:")}")

    @commands.command(name="toggle_hourly_phrase", description="Toggles the bot's functionality to repeat the phrase 'Trans Rights' every hour")
    async def toggle_hourly_phrase(self, ctx: discord.ext.commands.Context):
        if not self.__hourly_phrase_toggle: #function will only do anything if the bot has not been already set to repeat the phrase
            await bot.wait_until_ready() #wait for bot to be ready before starting a loop
            channel_id = ctx.message.channel.id
            channel = bot.get_channel(channel_id)

            while not bot.is_closed():
                await ctx.send(f"{emoji_list.get(":transgender_symbol:")}Trans Rights!{emoji_list.get(":transgender_flag:")}") 
                self.__hourly_phrase_toggle = True #toggle the hourly phrase in case the command is called again
                await asyncio.sleep(3600) #set the phrase to send every 1 hour (3600 seconds)

       



async def main():
    async with bot:
        await bot.add_cog(ResourceBot(bot))
        print("Cog added")
        await bot.start(BOT_TOKEN)


bot = ResourceBot()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

import asyncio
asyncio.run(main())

