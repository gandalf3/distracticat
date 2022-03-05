from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

Base = orm.declarative_base()


def unix_timestamp():
    return int(datetime.utcnow().timestamp())


class Distraction(Base):
    __tablename__ = "distraction"

    id = sa.Column(sa.Integer, primary_key=True)
    guild_id = sa.Column(sa.Integer, nullable=False)
    timestamp = sa.Column(sa.Integer, default=unix_timestamp)
    description = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer)
    message_id = sa.Column(sa.Integer)
