import discord
import asyncio
from main import client


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


