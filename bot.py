"""
bot.py - Main script for Community Resource Discord Bot

This bot provides curated community resources, allows users to profile information (e.g. name, pronouns, age, etc), 
and integrates external API for attribute lookup
It handles slash commands and ensures accessibility for all users.
"""

import discord
import logging
#import discord.ext.commands
import discord.ext.commands.bot as bot
from discord.ext import commands as ext_commands
import asyncio
from discord import app_commands
from discord.app_commands import commands
import discord.ext
import json
from typing import Optional
from api.external_api import fetch_data, fetch_pronoun_data, pronoun_look_up
import re
import sqlite3
import random
#from PIL import Image
#import requests
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
#intents.message_content = True
settings_file = "config/settings.json"

try:
    with open(settings_file, "r") as file:
        settings = json.load(file)

except FileNotFoundError:
    settings = {"hourly_phrase_repeat_feature": False}

def save_settings():
    with open(settings_file, "w") as file:
        json.dump(settings, file)

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = os.getenv("DEFAULT_GUILD_ID")

class ResourceBot(bot.Bot):
    """A Discord bot that provides curated resources for online communities.

    Users can register profile information, retrieve resource links, and access supportive tools.
    It supports slash commands for easy interaction.
    """

    def __init__(self):
        """Initializes the bot with the required intents and command tree setup, also toggles the hourly phrase."""
        super().__init__(command_prefix = '!', intents = intents)
        #self.__hourly_phrase_toggle = False #will be for toggling the hourly phrase in a later function

    '''@property
    async def _hourly_phrase_toggle(self):
        """A getter method for toggling the state of the hourly phrase """
        return self.__hourly_phrase_toggle'''

    async def setup_hook(self):
        print("Setting up...")
        try:
            self.tree.clear_commands(guild=discord.Object(id=GUILD_IDS))
            self.tree.copy_global_to(guild=discord.Object(id = GUILD_IDS))
            await self.tree.sync()
            #await self.tree.sync(guild=discord.Object(id = GUILD_IDS))  
            print("Commands synced") 
        except Exception as e:
            print(f"Error during command sync: {e}")

    async def on_ready(self):
        await self.wait_until_ready()  # ✅ Ensure bot is fully initialized
        print(f"✅ Logged in as {self.user}!")
        print(f"📜 Connected to Guilds: {[guild.name for guild in self.guilds]}")


        
class MyCog(ext_commands.Cog): 
    """
    A class that defines the collection of commands that the bot will respond to, inheriting from the Cog class from discord.ext.

    The commands range from listeners that prompt the bot to respond to certain phrases 
    (such as 'heat from fire') to slash commands that allow the user to register their 
    personal information for easy use.
    """ 
    def __init__(self, bot: ResourceBot):
        """Initializes the Cog class and an instance of our ResourceBot object called bot.
        
        Args:
            bot (ResourceBot): The instance of the resource bot that we pass in main() to run the bot
        """
        self.bot = bot

    @app_commands.command(name= "resources", description="Show curated resource links by category")
    @app_commands.describe(category = "Select the type of resource you wish to view")
    @app_commands.choices(category = [
        app_commands.Choice(name = "Pronoun Resources", value = "pronoun_resources"),
        app_commands.Choice(name = "Mental Health Support", value = "support"),
        app_commands.Choice(name = "Pronoun Information", value = "pronoun_information")
    ])
    async def resources(self, ctx: discord.Interaction, category: app_commands.Choice[str]):
        data = settings["resource_links"].get(category.value, [])
        if not data:
            await ctx.response.send_message(f"No links found for the following category: {category.name}.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title = f"Resources: {category.name}",
            color=discord.Color.blurple()
        )

        for item in data:
            embed.add_field(name=item["title"], value=item["url"], inline=False)

        await ctx.response.send_message(embed=embed)
    
    '''@app_commands.command(name="pronouns", description="Sends links to sites where you can explore pronouns")
    async def pronouns(self, ctx: discord.Interaction):
        await ctx.response.send_message("https://pronoundb.org/ \n https://en.pronouns.page/")

    @app_commands.command(name="explain_neopronouns", description="Sends an embed that has a brief summary of what neopronouns are and when they're used")
    async def explain_neopronouns(self, ctx: discord.Interaction):
        await ctx.response.send_message(embed= discord.Embed(title="What are neopronouns", description="""Neopronouns are a subset of pronouns that
        are outside those conventional in language. These pronouns are essentially limitless, as represent a wide range of diverse nonbinary identities
        Examples include: ze/zir/zirs and fae/faer/faers.\n\n
        For more reading visit the following resources: https://dictionary.cambridge.org/us/dictionary/english/neopronoun \n
        https://www.thetrevorproject.org/research-briefs/pronouns-usage-among-lgbtq-youth/
        """, color=discord.Color.blurple()))

    @app_commands.command(name="help_me", description="Sends links to sites and resources for LGBTQ+ friendly mental health")
    async def help_me(self, ctx: discord.Interaction):
        await ctx.response.send_message("""Please go to: Trevor Project (US): https://www.thetrevorproject.org \n
                       Trans Lifeline (US/Canada): https://translifeline.org \n 
                       or LGBT Foundation (UK): https://lgbt.foundation for mental health support.""")
        
    @app_commands.command(name="haircut", description="Sends a link that allows users to find trans-friendly hair places :3")
    async def haircut(self, ctx: discord.Interaction):
        await ctx.response.send_message("https://strandsfortrans.org/")

    @app_commands.command(name="read_books", description="Sends a resource for trans literature")
    async def read_books(self, ctx: discord.Interaction):
        await ctx.response.send_message("https://transreads.org/")'''

    #TO DO: 1) modify how the function uses defer() in order to accomodate stress_test_commands(), 2) Delete the current data for user_id for discord account
    @app_commands.command(name="register", description="Register your pronouns and info (note a link will override other info)")
    @app_commands.describe(link="Your pronouns.page link",
    name="Your preferred name",
    pronouns="Your pronouns (e.g., they/them)",
    age="Your age (optional)")
    async def register(self, ctx: discord.Interaction, link: Optional[str], name:  Optional[str],
    pronouns: Optional[str], age: Optional[int]):
        if not ctx.response.is_done():
            await ctx.response.defer()
        await asyncio.sleep(5)
        bot_message = ""
        discord_user = ctx.user.name
        server_id = ctx.guild_id
        server_name = ctx.guild.name
        if not name and not link:
            user_data = None
        else:
            user_data = await MyCog.verify(self, ctx, link, name, pronouns, age)

        if user_data and user_data["age"] > 0:
            try:
                connection = sqlite3.connect("db/user_data.db")
                cursor = connection.cursor()
                cursor.execute(f"""INSERT INTO Users (name,pronouns,age,user_id,server_id) 
                            VALUES (:name,:pronouns,:age,:user_id,:server_id)
                            """, user_data)
                cursor.execute("SELECT * FROM Servers WHERE server_id = ?", (server_id,))
                result = cursor.fetchone()

                if not result:
                    cursor.execute("""
                    INSERT INTO Servers(server_name, server_id)
                    VALUES (?,?)
                    """, (server_name, server_id))

                connection.commit()

                bot_message = f"Data for user {discord_user} sucessfully added!"

            except sqlite3.Error as e:
                # Roll back in case of an error
                bot_message = f"An error occurred: {e}"
                connection.rollback()

            finally:
                connection.close()
        
        elif user_data == {}: 
            bot_message = "Error: Invalid link"
        elif not user_data:
            if not name:
                bot_message = "Error: No name"
            else:
                bot_message = "Error: Unknown pronouns"
        elif age <= 0:
            bot_message = "Error: age cannot be 0 or less."

        await ctx.followup.send(bot_message)
    
    async def verify(self, ctx: discord.Interaction, link: Optional[str], name:  Optional[str],
    pronouns: Optional[str], age: Optional[int]):
        discord_user = ctx.user.name
        server_id = ctx.guild_id
        user_data = {}
        found_valid_link = False
        links = settings["language_versions"]
        
        if link: 
            for key, value in links.items():
                url_format = fr"{key}/(?:@|u/)([\w-]+)$"
                matched_link = re.match(url_format, link)
                if matched_link:
                    settings["user_language_card"] = value
                    username = matched_link.group(1)
                    user_data = await fetch_data(key, {"username" : username})
                    user_data.update({"user_id": discord_user, "server_id": server_id})
                    found_valid_link = True
                    save_settings()
                    break
            
            if pronouns and not found_valid_link:
                user_data = await MyCog.try_manual_info(name, pronouns, age, discord_user, server_id)

        else:
            user_data = await MyCog.try_manual_info(name, pronouns, age, discord_user, server_id)
        return user_data

    async def try_manual_info(name:  Optional[str], pronouns: Optional[str], age: Optional[int],
    discord_user: str, server_id: str):
        if pronouns:
            link_type = await pronoun_look_up(pronouns)
            if link_type:
                pronouns = await fetch_pronoun_data(link_type, pronouns)
            
        return {"name": name, "pronouns": pronouns, "age": age, "user_id": discord_user, "server_id": server_id}
       
    
    @app_commands.command(name="edit_info", description="Register your pronouns and info")
    @app_commands.describe(link="Your new pronouns.page link",
    name="Your updated preferred name",
    pronouns="Your updated pronouns (e.g., they/them)",
    age="Your updated age (optional)")
    async def edit_info(self, ctx: discord.Interaction, link: Optional[str], name:  Optional[str],
    pronouns: Optional[str], age: Optional[int]):
        await ctx.response.defer()
        await asyncio.sleep(5)
        discord_user = ctx.user.name
        server_id = ctx.guild_id
        server_name = ctx.guild.name
        updated_data = await MyCog.verify(self, ctx, link, name, pronouns, age)

        if updated_data and (not updated_data["age"] or updated_data["age"] > 0):
            try:
                connection = sqlite3.connect("db/user_data.db")
                cursor = connection.cursor()
                cursor.execute(f"SELECT name, pronouns, age FROM Users WHERE user_id = ?", (discord_user,))
                current_data = cursor.fetchone()
                
                index = 0
                for key, value in updated_data.items():
                    if not value:
                        updated_data[key] = current_data[index]
                    index += 1

                await ctx.followup.send(f"""Your current information: \n
                - Name: {current_data[0]}
                - Pronouns: {current_data[1]}
                - Age: {current_data[2]}
                \n
                """)

                await ctx.followup.send(f"""You want to update your information to: \n
                - Name: {updated_data["name"] } 
                - Pronouns: {updated_data["pronouns"]}
                - Age: {updated_data["age"]}
                \n
                """)

                await ctx.followup.send("Would you like to proceed? (yes/no)")

                def check(message):
                    return message.author == ctx.user and message.content.lower() in ["yes", "no"]

                try:
                    response = await my_bot.wait_for("message", check=check, timeout=60)
                    if response.content.lower() == "no":
                        await ctx.followup.send("No changes were made to your information.")
                        return
                except TimeoutError:
                    await ctx.followup.send("Error: timed out")
                    return 
                
                cursor.execute(f"""UPDATE Users 
                                SET name = ?, pronouns = ?, age = ?
                                WHERE user_id = ?;""", (updated_data["name"], updated_data["pronouns"], updated_data["age"], discord_user, ))
                connection.commit()
                await ctx.followup.send("Your information has been updated!")

            except sqlite3.Error as e:
                # Roll back in case of an error
                print(f"An error occurred: {e}")
                connection.rollback()

            finally:
                connection.close()

        elif updated_data == {}: 
            await ctx.followup.send("Error: Invalid link")
        elif not updated_data:
            await ctx.followup.send("Error: Unknown pronouns")
        elif age <= 0:
            await ctx.followup.send("Error: age cannot be 0 or less.")

        

    @app_commands.command(name="send_info", description="""Sends user information and crafts an example sentence using the user's name and pronoun information""")
    async def send_info(self, ctx: discord.Interaction):
        try:
            connection = sqlite3.connect("db/user_data.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT name, pronouns, age FROM Users WHERE user_id = ?", (ctx.user.name, ))
            user_info = cursor.fetchone()

            names = user_info[0].split("/")
            pronouns = user_info[1].split(",")
            
            identity_weights = [0.2] * len(names)
            identity_weights[0] = 0.8

            name = random.choices(names, identity_weights, k=1)
            pronouns = random.choices(pronouns, identity_weights,k=1)

            pronoun_form = []
            for pronoun in pronouns:
                pronoun_form = pronoun.split("/")

            sentences = [
            f"{name[0].capitalize()} said {pronoun_form[0]} would help.",
            f"I saw {name[0]} yesterday, and I asked {pronoun_form[1]} about it.",
            f"This is {name[0]}'s book; it's {pronoun_form[2]} favorite.",
            f"Did you see {name[0]}? {pronoun_form[0].capitalize()} is wearing a new outfit today.",
            f"{name[0].capitalize()} always takes care of {pronoun_form[4]}."
            ]

            example_sentence = random.choice(sentences)

            embed = discord.Embed(title=f"{ctx.user}'s Information", description=f"""
                    Name: {names} \n
                    Pronouns: {"/".join(pronouns)}\n
                    Age: {user_info[2]} \n
                    Example Sentence: {example_sentence}""", 
                    color=discord.Color.blurple())
            
            await ctx.response.send_message(embed=embed)

        except sqlite3.Error as e:
            # Roll back in case of an error
            print(f"An error occurred: {e}")
            connection.rollback()
        
        finally:
            connection.close()


    @app_commands.command(name="help", description="Displays all available commands.")
    async def help(self, ctx: discord.Interaction):
        embed = discord.Embed(title="Command List", color=discord.Color.blurple())

        for cmd in self.bot.tree.get_commands():
            embed.add_field(name=cmd.name, value=cmd.description, inline=False)

        embed.set_footer(text="Use / before each command to run it")

        await ctx.response.send_message(embed=embed)

    @app_commands.command(name = "ping", description="Check if bot is alive and its latency")
    async def ping(self, ctx: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await ctx.response.send_message(f"Pong! Latency: {latency} ms")

async def main():
    async with my_bot:
        await my_bot.add_cog(MyCog(my_bot))
        print("Cog added")
        await my_bot.start(BOT_TOKEN)


my_bot = ResourceBot()

if __name__ == "__main__":
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    logging.basicConfig(level=logging.INFO, handlers=[handler])


    asyncio.run(main())

