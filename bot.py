#!/usr/bin/env python3

import logging
import os
import random
import sys

import discord
import yaml

import sqlalchemy as sa
from sqlalchemy import orm

from discord.ext import commands

from distracticat import chooser, model
from distracticat.config import Config
from distracticat.emotes import Reactions

logging.basicConfig(level=logging.INFO)
log = logging

config = Config()

database_url = os.environ["DATABASE_URL"]
engine: sa.engine.Engine = sa.create_engine(database_url, echo=True, future=True)


bot = commands.Bot(command_prefix=config.command_prefix)


async def add_distraction(
    distraction: model.Distraction,
    channel: discord.PartialMessageable,
    reply,
):
    await channel.send(Reactions.reaction())

    embed = discord.Embed(
        title="new distraction!",
        description=distraction.description,
        color=discord.Color.purple(),
    )
    embed.add_field(name="Suggested by", value=f"<@{distraction.author_id}>")

    async with channel.typing():
        with orm.Session(engine) as session:
            session.add(distraction)
            session.commit()

    await reply(embed=embed)


@bot.command(name="distracticat")
async def distracticat_cmd(ctx: commands.Context, *, description: str):
    author_id, message_id = ctx.author.id, ctx.message.id
    distraction = model.Distraction(
        guild_id=ctx.guild.id,
        description=description,
        author_id=author_id,
        message_id=message_id,
    )
    await add_distraction(distraction, ctx.channel, ctx.reply)


@bot.slash_command(name="distracticat", guild_ids=config.guild_ids())
async def distracticat_scmd(ctx: discord.ApplicationContext, description: str):
    author_id = ctx.author.id
    distraction = model.Distraction(
        guild_id=ctx.guild.id,
        description=description,
        author_id=author_id,
    )
    await add_distraction(distraction, ctx.channel, ctx.respond)


@bot.command(name="commitfelicide")
async def kill(ctx: commands.Context):
    await ctx.reply("how could you do this? (ಡ‸ಡ)")
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


with open("secret.yaml") as f:
    secret_token = yaml.safe_load(f)["token"]

bot.run(secret_token)
