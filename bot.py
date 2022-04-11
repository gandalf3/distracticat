#!/usr/bin/env python3

import logging
import os
import random
import sys

import discord

from dotenv import load_dotenv

import sqlalchemy as sa
from sqlalchemy import orm

from discord.ext import commands

from distracticat import chooser, model
from distracticat.config import Config
from distracticat.emotes import Reactions

logging.basicConfig(level=logging.INFO)
log = logging

load_dotenv()


def getenv(key: str) -> str:
    if (value := os.getenv(key)) is not None:
        return value
    else:
        exit(f"{key} environment variable not specified")


database_url = getenv("DATABASE_URL")
discord_secret_token = getenv("DISCORD_SECRET_TOKEN")

config = Config()
bot = commands.Bot(command_prefix=config.command_prefix)

engine: sa.engine.Engine = sa.create_engine(database_url, echo=True, future=True)


async def add_distraction(
    channel: discord.PartialMessageable,
    reply,
    description: str,
    guild_id: int,
    author_id: int,
    message_id: int | None = None,
):
    await channel.send(Reactions.reaction())

    distraction = model.Distraction(
        guild_id=guild_id,
        description=description,
        author_id=author_id,
        message_id=message_id,
    )

    embed = discord.Embed(
        title="new distraction!",
        description=distraction.description,
        color=discord.Color.purple(),
    )
    embed.add_field(name="Suggested by", value=f"<@{author_id}>")

    async with channel.typing():
        with orm.Session(engine) as session:
            session.add(distraction)
            session.commit()

    await reply(embed=embed)


@bot.command(name="distracticat")
async def distracticat_cmd(ctx: commands.Context, *, description: str):
    await add_distraction(
        ctx.channel,
        ctx.reply,
        description,
        ctx.guild.id,
        ctx.author.id,
        ctx.message.id,
    )


@bot.slash_command(name="distracticat", guild_ids=config.guild_ids())
async def distracticat_scmd(ctx: discord.ApplicationContext, description: str):
    await add_distraction(
        ctx.channel,
        ctx.respond,
        description,
        ctx.guild.id,
        ctx.author.id,
    )


@bot.command(name="commitfelicide")
async def kill_cmd(ctx: commands.Context):
    await ctx.reply("how could you do this? (ಡ‸ಡ)")
    sys.exit()


@bot.slash_command(name="commitfelicide", guild_ids=config.guild_ids())
async def kill_scmd(ctx: commands.Context):
    await ctx.respond("how could you do this? (ಡ‸ಡ)")
    sys.exit()


@bot.command()
async def choose(ctx: commands.Context, *, choices_str: str):
    choices, feedback = chooser.parse_choices(choices_str)

    if feedback:
        await ctx.send(feedback)
        return

    if len(choices) == 0:
        await ctx.reply(
            "That's a tough decision you're asking me to make you know. "
            "Let me get back to you on that one."
        )
        return

    if len(choices) == 1:
        await ctx.reply(f"That's a sound decision {ctx.author}")
    else:
        chosen = random.choice(choices)
        await ctx.reply(f"Hm.. :thinking: I say go with {chosen}.")


@bot.event
async def on_ready():
    log.info(f"logged in as {bot.user}")


bot.run(discord_secret_token)
