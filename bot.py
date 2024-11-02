import discord
from discord.ext import commands
import logging
import discord.ext.commands.bot
from emoji_list import EmojiList

intents = discord.Intents.default()
emoji_list = EmojiList()

guild_ids = GUILD_IDS
discord_token = DISCORD_TOKEN


class ResourceBot(commands.Bot):
    def __init__(self, bot):
        super().__init__(command_prefix = '!', intents = intents)
        self.bot = bot
        #self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        print("Setting up...")
        try:
            self.tree.clear_commands(guild=discord.Object(id=guild_ids))
            self.tree.copy_global_to(guild=discord.Object(id = guild_ids))
            await self.tree.sync(guild=discord.Object(id = guild_ids))  
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

        for cop_phrase in cop_trigger_phrases:
            if cop_phrase in [word for word in message.content.split(" ").lower()]:
                await message.channel.send(f"ACAB! {emoji_list.get(":police_officer:")} 
                {emoji_list.get(":heavy_equals_sign:")} {emoji_list.get(":pig:")}")

        if heat_from_fire in [word for word in message.content.split(" ").lower()]:
            await message.channel.send("Heat from fire! :3")

        for nazi_phrase in nazi_trigger_phrases:
            if nazi_phrase in [word for word in message.content.split(" ").lower()]:
                await message.channel.send(f"Punch a Nazi {emoji_list.get(":punch:")}")



async def main():
    async with bot:
        await bot.add_cog(ResourceBot(bot))
        print("Cog added")
        await bot.start(discord_token)


bot = ResourceBot()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

import asyncio
asyncio.run(main())

