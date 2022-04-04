from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Server:
    name: str
    guild_id: int


class Config:
    servers: list[Server]

    command_prefix: str

    def __init__(self, path=Path("config.yaml")):
        with open(path) as f:
            raw_config = yaml.safe_load(f)

        self.servers = [
            Server(name=sv["name"], guild_id=int(sv["guild_id"]))
            for sv in raw_config["servers"]
        ]

        self.command_prefix = raw_config["command_prefix"] or "!"

    def guild_ids(self) -> list[int]:
        return [sv.guild_id for sv in self.servers]
