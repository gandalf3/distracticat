#!/usr/bin/env python3

import asyncio
import discord
from discord.ext import commands
import logging
import json
import random

logging.basicConfig(level=logging.INFO)
log = logging


with open("config.json") as f:
    config = json.load(f)
    servers = config["servers"].values()
with open("secret.json") as f:
    secrets = json.load(f)
    secret_token = secrets["token"]

with open("reactions.txt") as f:
    reactions = f.read().splitlines()
with open("noises.txt") as f:
    noises = f.read().splitlines()

bot = commands.Bot(command_prefix="!")


@bot.command()
async def distracticat(ctx: commands.Context, *, distraction: str):
    async def sleep_type(sleep_time, type_time):
        await asyncio.sleep(sleep_time)
        async with ctx.channel.typing():
            await asyncio.sleep(type_time)

    await sleep_type(0.2, 0.3)
    await ctx.channel.send(
        random.choice(reactions).replace("<noise>", random.choice(noises))
    )

    await sleep_type(0.5, 0.3)
    embed = discord.Embed(
        title="new distraction!", description=distraction, color=discord.Color.purple()
    )
    await ctx.message.reply(embed=embed)


@bot.slash_command(guild_ids=servers)
async def distracticat_scmd(ctx: discord.ApplicationContext, number: int):
    await ctx.respond(number)


@bot.event
async def on_ready():
    log.info(f"logged in as {bot.user}")


bot.run(secret_token)
