from unittest.mock import AsyncMock
import pytest

import discord
from discord import app_commands

from types import SimpleNamespace

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from bot import MyCog, settings


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

@pytest.mark.asyncio
async def test_mental_health_support():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock())
    )

    support_resources = app_commands.Choice(name="Mental Health Support", value="support")
    embed = await get_embed(support_resources.name, support_resources.value)
    
    if embed:
        await MyCog.resources.callback(cog, ctx, support_resources)
        ctx.response.send_message.assert_awaited_once_with(embed=embed)

@pytest.mark.asyncio
async def test_pronoun_info():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock())
    )

    pronoun_info = app_commands.Choice(name="Pronoun Information", value="pronoun_information")
    embed = await get_embed(pronoun_info.name, pronoun_info.value)
    
    if embed:
        await MyCog.resources.callback(cog, ctx, pronoun_info)
        ctx.response.send_message.assert_awaited_once_with(embed=embed)

@pytest.mark.asyncio
async def test_non_option():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock())
    )

    non_option = app_commands.Choice(name="Not An Option", value="not_an_option")
    embed = await get_embed(non_option.name, non_option.value)

    if embed:
        raise AssertionError
    else: 
        await MyCog.resources.callback(cog, ctx, non_option)
        message = f"No links found for the following category: {non_option.name}."
        ctx.response.send_message.assert_awaited_once_with(message, ephemeral=True)

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