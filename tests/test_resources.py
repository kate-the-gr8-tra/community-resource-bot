from unittest.mock import Mock, AsyncMock
import pytest

import discord
import asyncio
from discord import app_commands

from bot import ResourceBot, MyCog, main, settings

import os

bot = ResourceBot()

#BOT_TOKEN = os.getenv("DISCORD_TOKEN")

@pytest.fixture
def mock_ctx() -> Mock:
    mock = Mock()
    mock.send = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_pronoun_resource(mock_ctx):
    cog_instance = get_cog()
    if cog_instance:
        pronoun_option = app_commands.Choice(name="Pronoun Resources", value="pronoun_resources")
        await cog_instance.resources(mock_ctx, pronoun_option)
        data = settings["resource_links"]["pronoun_resources"]
        embed = discord.Embed(
            title=f"Resources: Pronoun Resources", color=discord.Color.blurple()
        )

        for item in data:
            embed.add_field(name=item["title"], value=item["url"], inline=False)

        mock_ctx.send.assert_awaited_once_with(embed)

def get_cog() -> MyCog:
    return bot.get_cog("MyCog")

if __name__ == "__main__":
    asyncio.run(main())