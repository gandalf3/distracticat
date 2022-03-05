#!/usr/bin/env python3

import logging
import random

import discord
import yaml

import sqlalchemy as sa
from sqlalchemy import orm

from discord.ext import commands

from bot.config import Config
from bot import model

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


@bot.event
async def on_ready():
    log.info(f"logged in as {bot.user}")


with open("secret.yaml") as f:
    secret_token = yaml.safe_load(f)["token"]

bot.run(secret_token)
