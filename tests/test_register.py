from unittest.mock import AsyncMock
import pytest

import discord
from discord import app_commands

from types import SimpleNamespace
from typing import Optional

import sqlite3

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from bot import MyCog, DB_PATH, GUILD_ID

@pytest.mark.asyncio
async def test_successful_register1():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(is_done = AsyncMock(), defer = AsyncMock()),
        followup = SimpleNamespace(send = AsyncMock()),
        user = discord.User,
        guild_id = int,
        guild = discord.Guild
    )

    ctx.user.name = "alice1"
    ctx.user.id = 1234567890
    ctx.guild_id = GUILD_ID
    ctx.guild.name = "bleh"

    info = {
        "name" : "Alice",
        "pronouns" : "she/her",
        "age" : 19
    }

    vals = list(info.values())

    desired_response = f"""Data for user {ctx.user.name} sucessfully added!\nNote: This bot stores your profile (name, pronouns, age, Discord ID, and server ID) 
                so it can respond to commands like /send_info.
                You can update it anytime with /register or /edit_info, and you can remove it completely with 
                /delete_info."""
    
    await MyCog.register.callback(cog, ctx, None, *vals)
    ctx.followup.send.assert_awaited_once_with(desired_response, ephemeral=True)

    present_data = await check_data(ctx.user.id)
    if present_data[0] != "Alice" or present_data[1] != "she/her/her/hers/herself" or present_data[2] != 19:
        raise AssertionError

    await delete_temp_data()

@pytest.mark.asycio
async def test_successful_register2():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    link = "https://en.pronouns.page/@pabisox764"

    desired_response =  f"""Data for user {ctx.user.name} sucessfully added!\nNote: This bot stores your profile (name, pronouns, age, Discord ID, and server ID) 
                so it can respond to commands like /send_info.
                You can update it anytime with /register or /edit_info, and you can remove it completely with 
                /delete_info."""
    
    await MyCog.register.callback(cog, ctx, link)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    present_data = await check_data(ctx.user.id)
    if present_data[0] != "Alice" or present_data[1] != "she/her/her/hers/herself" or present_data[2] != 19:
        raise AssertionError

    await delete_temp_data()

@pytest.mark.asycio
async def test_successful_register3():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    link = "https://en.pronouns.page/@pabisox764"
    info = {
        "name" : "Bob",
        "pronouns" : "he/him",
        "age" : 18
    }

    vals = list(info.values())

    desired_response =  f"""Data for user {ctx.user.name} sucessfully added!\nNote: This bot stores your profile (name, pronouns, age, Discord ID, and server ID) 
                so it can respond to commands like /send_info.
                You can update it anytime with /register or /edit_info, and you can remove it completely with 
                /delete_info."""
    
    await MyCog.register.callback(cog, ctx, link, *vals)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    present_data = await check_data(ctx.user.id)
    if present_data[0] != "Alice" or present_data[1] != "she/her/her/hers/herself" or present_data[2] != 19:
        raise AssertionError

    await delete_temp_data()

@pytest.mark.asycio
async def test_failed_register1():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    info = {
        "pronouns" : "she/her",
        "age" : 19
    }

    vals = list(info.values())

    desired_response = "Error: No name."

    await MyCog.register.callback(cog, ctx, None, None, *vals)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    if await check_data(ctx.user.id) is not None:
        raise AssertionError

@pytest.mark.asycio
async def test_failed_register2():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    info = {
        "name" : "Alice",
        "pronouns" : "she/her",
        "age" : -19
    }

    vals = list(info.values())

    desired_response = "Error: age cannot be 0 or less."

    await MyCog.register.callback(cog, ctx, None, *vals)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    if await check_data(ctx.user.id) is not None:
        raise AssertionError
    
    
@pytest.mark.asycio
async def test_failed_register3():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    link = "bad link"

    desired_response = "Error: Invalid link."

    await MyCog.register.callback(cog, ctx, link)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    if await check_data(ctx.user.id) is not None:
        raise AssertionError
    
@pytest.mark.asycio
async def test_failed_register4():
    cog = MyCog(bot=None)
    ctx = SimpleNamespace(
        response = SimpleNamespace(send_message = AsyncMock()),
        user = discord.User(name = "alice1", id = 1234567890)
    )

    info = {
        "name" : "Alice",
        "pronouns" : "unknown pronouns",
        "age" : 19
    }
    vals = list(info.values())

    desired_response = "Error: Unknown pronouns, you can register them on pronouns.page."

    await MyCog.register.callback(cog, ctx, None, *vals)
    ctx.response.send_message.assert_awaited_once_with(desired_response, ephemeral=True)

    if await check_data(ctx.user.id) is not None:
        raise AssertionError

async def check_data(discord_id: int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT name, pronouns, age FROM Users WHERE user_id = ?",
            (discord_id,),
        )
        return cursor.fetchone()
    
    except sqlite3.Error as e:
            # Roll back in case of an error
            print(f"An error occurred: {e}")
            connection.rollback()

    finally:
        connection.close()

async def delete_temp_data():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Users")
        connection.commit()
    except sqlite3.Error as e:
            # Roll back in case of an error
            print(f"An error occurred: {e}")
            connection.rollback()

    finally:
        connection.close()