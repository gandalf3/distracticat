#!/usr/bin/env python3

import logging
import random
import time

import discord
import yaml

import sqlalchemy as sa
import sqlalchemy.orm as orm

from discord.ext import commands

logging.basicConfig(level=logging.INFO)
log = logging

engine: sa.engine.Engine = sa.create_engine(
    "sqlite+pysqlite:///database.db", echo=True, future=True
)

mapper_registery = orm.registry()
Base = mapper_registery.generate_base()


class Distraction(Base):
    __tablename__ = "distraction"

    id = sa.Column(sa.Integer, primary_key=True)
    guild_id = sa.Column(sa.Integer, nullable=False)
    timestamp = sa.Column(sa.Integer)
    description = sa.Column(sa.String)


class Server:
    name: str
    guild_id: int

    def __init__(self, name: str, guild_id: int):
        self.name = name
        self.guild_id = guild_id


with open("config.yaml") as f:
    config = yaml.safe_load(f)

servers = [Server(sv["name"], sv["guild_id"]) for sv in config["servers"]]

guild_ids = [s.guild_id for s in servers]

with open("secret.yaml") as f:
    secrets = yaml.safe_load(f)
    secret_token = secrets["token"]

with open("reactions.txt") as f:
    reactions = f.read().splitlines()
with open("noises.txt") as f:
    noises = f.read().splitlines()

bot = commands.Bot(command_prefix="!")


@bot.command()
async def distracticat(ctx: commands.Context, *, description: str):
    await ctx.channel.send(
        random.choice(reactions).replace("<noise>", random.choice(noises))
    )

    async with ctx.channel.typing():
        distraction = Distraction(
            guild_id=ctx.guild.id, timestamp=int(time.time()), description=description
        )
        with orm.Session(engine) as session:
            session.add(distraction)
            session.commit()

    embed = discord.Embed(
        title="new distraction!", description=description, color=discord.Color.purple()
    )
    await ctx.message.reply(embed=embed)


# @bot.slash_command(guild_ids=guild_ids)
# async def distracticat_scmd(ctx: discord.ApplicationContext):
#     pass


@bot.event
async def on_ready():
    log.info(f"logged in as {bot.user}")


bot.run(secret_token)
