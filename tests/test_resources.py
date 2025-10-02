from unittest.mock import Mock, AsyncMock
import pytest
import pytest_asyncio

import discord
import asyncio
from discord import app_commands

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from bot import ResourceBot, MyCog, main, settings



bot = ResourceBot()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

@pytest.fixture(autouse=True, scope="module")
def mock_ctx() -> Mock:
    mock = Mock()
    mock.send = AsyncMock()
    return mock

@pytest.fixture(autouse=True, scope="module")
async def load_cog():
    #print("Hi from before any test")
    bot.run(BOT_TOKEN)
    print(f"Testing as {bot.user}")
    await bot.load_extension("bot")
    print("Cog loaded successfully")


@pytest_asyncio.is_async_test
async def test_pronoun_resource(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed=check(mock_ctx, "Pronoun Resources", "pronoun_resources", cog_instance))
    else: 
        raise AssertionError


@pytest_asyncio.is_async_test
async def test_mental_health_support(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed=check(mock_ctx, "Mental Health Support", "support", cog_instance))
    else: 
        raise AssertionError

@pytest_asyncio.is_async_test
async def test_pronoun_info(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed=check(mock_ctx, "Pronoun Information", "pronoun_information", cog_instance))
    else: 
        raise AssertionError

@pytest_asyncio.is_async_test
async def test_non_option(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        choice = app_commands.Choice(name="Not A Resource", value="not_a_resource_value")
        await cog_instance.resources(mock_ctx, choice)
        mock_ctx.send.assert_awaited_once_with("No links found for the following category: Not A Resource.",
        ephemeral=True)
    else: 
        raise AssertionError

    

async def check(mock, resource_name: str, resource_val: str, my_cog: MyCog) -> discord.Embed:
    choice = app_commands.Choice(name=resource_name, value=resource_val)
    await my_cog.resources(mock, choice)
    data = settings["resource_links"][resource_val]
    embed = discord.Embed(
        title=f"Resources: {resource_name}", color=discord.Color.blurple()
    )

    for item in data:
        embed.add_field(name=item["title"], value=item["url"], inline=False)

    return embed

'''@bot.event
async def on_ready():
    print(f"Testing as {bot.user}")
    await bot.load_extension("bot")
    print("Cog loaded successfully")'''

@pytest.mark.usefixtures("load_cog")
def get_cog() -> MyCog:
    
    #for cog in bot.cogs:
    #    print(cog)
    return bot.get_cog(MyCog(bot))

if __name__ == "__main__":
    pytest.main([__file__])
    bot.run(BOT_TOKEN)