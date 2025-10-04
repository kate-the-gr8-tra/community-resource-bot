from unittest.mock import AsyncMock
import pytest
import pytest_asyncio

import discord
from discord import app_commands

import asyncio
import contextlib
from types import SimpleNamespace

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from bot import MyCog, settings



#bot = ResourceBot()

#BOT_TOKEN = os.getenv("DISCORD_TOKEN")

'''@pytest_asyncio.fixture(autouse=True, scope="module")
def mock_ctx() -> Mock:
    mock = Mock()
    mock.send = AsyncMock()
    return mock'''

'''@pytest_asyncio.fixture(autouse=True, scope="module")
async def load_cog():
    #print("Hi from before any test")

    task = asyncio.create_task(bot.start(BOT_TOKEN))

    try:
        await asyncio.wait_for(bot.wait_until_ready(), timeout=15)
        print(f"Testing as {bot.user}")
        await bot.load_extension("bot")
        await bot.add_cog(MyCog(bot))
        print("Cog loaded successfully")
    except asyncio.InvalidStateError as e:
        print(f"Error: {e}")
    finally:
        await bot.close()
        await asyncio.sleep(10)
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
'''       

@pytest.mark.asyncio
async def test_pronoun_resource():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock())
    )

    pronoun_resources = app_commands.Choice(name="Pronoun Resources", value="pronoun_resources")
    embed = await get_embed(pronoun_resources.name, pronoun_resources.value)
    
    if embed:
        await MyCog.resources.callback(cog, ctx, pronoun_resources)
        ctx.response.send_message.assert_awaited_once_with(embed=embed)
    else:
        raise AssertionError

    

    '''cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed= await check(mock_ctx, "Pronoun Resources", "pronoun_resources", cog_instance))
    else: 
        raise AssertionError'''

@pytest.mark.asyncio
async def test_mental_health_support(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed= await check(mock_ctx, "Mental Health Support", "support", cog_instance))
    else: 
        raise AssertionError

@pytest.mark.asyncio
async def test_pronoun_info(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        mock_ctx.send.assert_awaited_once_with(embed= await check(mock_ctx, "Pronoun Information", "pronoun_information", cog_instance))
    else: 
        raise AssertionError

@pytest.mark.asyncio
async def test_non_option(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        choice = app_commands.Choice(name="Not A Resource", value="not_a_resource_value")
        await cog_instance.resources(mock_ctx, choice)
        mock_ctx.send.assert_awaited_once_with("No links found for the following category: Not A Resource.",
        ephemeral=True)
    else: 
        raise AssertionError

    

async def get_embed(resource_name: str, resource_val: str) -> discord.Embed:
    choice = app_commands.Choice(name=resource_name, value=resource_val)
    #await my_cog.resources(mock, choice)
    try:
        data = settings["resource_links"][resource_val]
        embed = discord.Embed(
            title=f"Resources: {resource_name}", color=discord.Color.blurple()
        )

        for item in data:
            embed.add_field(name=item["title"], value=item["url"], inline=False)

        return embed
    
    except KeyError:
        return None

'''@bot.event
async def on_ready():
    print(f"Testing as {bot.user}")
    await bot.load_extension("bot")
    print("Cog loaded successfully")'''


def get_cog() -> MyCog:
    
    #for cog in bot.cogs:
    #    print(cog)
    return bot.get_cog("MyCog")

if __name__ == "__main__":
    pytest.main([__file__])
    bot.run(BOT_TOKEN)