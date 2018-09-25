import discord
import asyncio
from bot_main import client


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


