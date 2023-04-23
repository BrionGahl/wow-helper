from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


Base = declarative_base()


class Guilds(Base):
    __tablename__ = 'guilds'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    wow_name: Mapped[str] = mapped_column(String(24))
    wow_server: Mapped[str] = mapped_column(String(24))


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey('guilds.id'))
    name: Mapped[str] = mapped_column(String(40))
    wow_name: Mapped[str] = mapped_column(String(24))
    wow_server: Mapped[str] = mapped_column(String(24))