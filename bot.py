#!/usr/bin/env python3

import logging
import random

import discord
import yaml

import sqlalchemy as sa
from sqlalchemy import orm

from discord.ext import commands

from distracticat.config import Config
from distracticat import chooser, model

logging.basicConfig(level=logging.INFO)
log = logging

config = Config()

engine: sa.engine.Engine = sa.create_engine(
    "sqlite+pysqlite:///database.db", echo=True, future=True
)


bot = commands.Bot(command_prefix=config.command_prefix)


@bot.command()
async def distracticat(ctx: commands.Context, *, description: str):
    author_id, message_id = ctx.author.id, ctx.message.id

    await ctx.channel.send(
        random.choice(config.reactions).replace("<noise>", random.choice(config.noises))
    )

    async with ctx.channel.typing():
        distraction = model.Distraction(
            guild_id=ctx.guild.id,
            description=description,
            author_id=author_id,
            message_id=message_id,
        )
        with orm.Session(engine) as session:
            session.add(distraction)
            session.commit()

    embed = discord.Embed(
        title="new distraction!", description=description, color=discord.Color.purple()
    )
    embed.add_field(name="Suggested by", value=f"<@{author_id}>")
    await ctx.message.reply(embed=embed)


# @bot.slash_command(guild_ids=config.guild_ids())
# async def distracticat_scmd(ctx: discord.ApplicationContext):
#     pass


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
