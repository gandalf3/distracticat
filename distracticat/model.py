from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

Base = orm.declarative_base()


def unix_timestamp():
    return int(datetime.utcnow().timestamp())


class Distraction(Base):
    __tablename__ = "distraction"

    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    description = sa.Column(sa.String)
    guild_id = sa.Column(sa.BigInteger)
    author_id = sa.Column(sa.BigInteger)
    message_id = sa.Column(sa.BigInteger)
