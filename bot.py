import discord
import logging
import discord.ext.commands
import discord.ext.commands.bot as bot
from discord.ext import commands as ext_commands
import asyncio
from discord import app_commands
from discord.app_commands import commands
import discord.ext
import json
from typing import Optional

intents = discord.Intents.default()
intents.message_content = True
settings_file = "settings/settings.json"

try:
    with open(settings_file, "r") as file:
        settings = json.load(file)

except FileNotFoundError:
    settings = {"hourly_phrase_repeat_feature": False}

def save_settings():
    with open(settings_file, "w") as file:
        json.dump(settings, file)


#~~~ TESTING SECTION ~~~
with open('info.txt', "r") as file:
    info_list = file.read().splitlines()
    GUILD_IDS = info_list[0]
    BOT_TOKEN = info_list[1]
#~~~ TESTING SECTION ~~~


class ResourceBot(bot.Bot):
    def __init__(self):
        super().__init__(command_prefix = '!', intents = intents)
        self.__hourly_phrase_toggle = False #will be for toggling the hourly phrase in a later function

    @property
    async def _hourly_phrase_toggle(self):
        return self.__hourly_phrase_toggle

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

class MyCog(ext_commands.Cog):  
    def __init__(self):
        super().__init__()
        self.bot = ResourceBot()

    # Override on_message event
    @ext_commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return #do nothing if message came from a bot
        
        cop_trigger_phrases = ["cop", "cops", "pigs", "pig", "police", "acab"]
        heat_from_fire = "heat from fire"
        nazi_trigger_phrases = ["nazi", "nazis" "fascist", "fascists" "fascism"]
        nazi_german_trigger = "nationalsozialistisch"

        for cop_phrase in cop_trigger_phrases:
            if cop_phrase in [word.lower() for word in message.content.split(" ")]:
                await message.channel.send("ACAB! :police_officer:" \
                "= :pig:") 

        if heat_from_fire == message.content.lower():
            await message.channel.send("Fire from heat! :3")

        for nazi_phrase in nazi_trigger_phrases:
            if nazi_phrase in [word.lower() for word in message.content.split(" ")]:
                await message.channel.send("MAKE THE WORLD A BETTER PLACE PUNCH A NAZI IN THE FACE! :punch:")

        if nazi_german_trigger in [word.lower() for word in message.content.split(" ")]:
            await message.channel.send("MACH DIE WELT EINEN BESSEREN ORT, SCHLAG EINEM NAZI INS GESICHT! :punch:")
    
    async def send_hourly_message(self, ctx: discord.Interaction, state: int):
        while not self.bot.is_closed():
            if state == 1:
                await ctx.response.send_message(":transgender_symbol: Trans Rights! :transgender_flag:") 
                settings["hourly_phrase_repeat_feature"] = True #toggle the hourly phrase in case the command is called again and store it in the json file
                save_settings()
                await asyncio.sleep(3600) #set the phrase to send every 1 hour (3600 seconds)
            elif state == 0:
                await ctx.response.send_message("Hourly phrase turned off.")
                settings["hourly_phrase_repeat_feature"] = False
                save_settings()
                raise asyncio.CancelledError("Hourly message task cancelled.")
            elif state == -1:
                await ctx.response.send_message("Error: State is already set to on/off")


    @app_commands.command(name="toggle_hourly_phrase", description="Toggles the bot's functionality to repeat the phrase 'Trans Rights' every hour")
    async def toggle_hourly_phrase(self, ctx: discord.Interaction, turn_on: bool):
        if not settings["hourly_phrase_repeat_feature"] and turn_on: 
            #function will only do anything if the bot has not been already set to repeat the phrase
            await MyCog.send_hourly_message(self,ctx,1) 
        elif settings["hourly_phrase_repeat_feature"] and not turn_on: 
            #case where the feature is on and the user turns it off
           await MyCog.send_hourly_message(self,ctx,0)
        elif settings["hourly_phrase_repeat_feature"] and turn_on or not settings["hourly_phrase_repeat_feature"] and not turn_on: 
            #cases where the user tries to turn on/off the feature but it's already in that state
            await MyCog.send_hourly_message(self,ctx,-1)
        
    
    @app_commands.command(name="pronouns", description="Sends links to sites where you can explore pronouns")
    async def pronouns(self, ctx: discord.Interaction):
        await ctx.response.send_message("https://pronoundb.org/ \n https://en.pronouns.page/")

    @app_commands.command(name="help_me", description="Sends links to sites and resources for LGBTQ+ friendly mental health")
    async def help_me(self, ctx: discord.Interaction):
        await ctx.response.send_message("Please go to: Trevor Project (US): https://www.thetrevorproject.org \n \
                       Trans Lifeline (US/Canada): https://translifeline.org \n \
                       or LGBT Foundation (UK): https://lgbt.foundation for mental health support.")
        
    
    @app_commands.command(name="register", description="Register your pronouns and info")
    @app_commands.describe(link="Your pronouns.page or pronoundb link",
    name="Your preferred name",
    pronouns="Your pronouns (e.g., they/them)",
    age="Your age (optional)")
    async def register(self, ctx: discord.Interaction, link: Optional[str], name:  Optional[str],
    pronouns: Optional[str], age: Optional[int]):
        discord_user = ctx.message.author.name
        if isinstance(link, None):
            pass
        elif isinstance(link, str):
            if "pronoundb.org" in link:
                pass  
            elif "en.pronouns.page" in link:
                pass
     

async def main():
    async with my_bot:
        await my_bot.add_cog(MyCog())
        print("Cog added")
        await my_bot.start(BOT_TOKEN)


my_bot = ResourceBot()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])


asyncio.run(main())

