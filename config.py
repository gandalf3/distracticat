from dataclasses import dataclass

import yaml


@dataclass
class Server:
    name: str
    guild_id: int


@dataclass
class Config:
    servers: list[Server]

    reactions: list[str]
    noises: list[str]

    @classmethod
    def load(cls):
        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        servers = [Server(sv["name"], sv["guild_id"]) for sv in config["servers"]]

        with open("reactions.txt") as f:
            reactions = f.read().splitlines()
        with open("noises.txt") as f:
            noises = f.read().splitlines()

        return cls(servers, reactions, noises)

    def guild_ids(self) -> list[int]:
        return [sv.guild_id for sv in self.servers]
