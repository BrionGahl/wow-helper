from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

"""
Stores information about various rows in the utilized table. In the future might break these down into multiple modules.
"""

Base = declarative_base()


class Guilds(Base):
    """Row Layout for the Guilds Table"""
    __tablename__ = 'guilds'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    wow_name: Mapped[str] = mapped_column(String(24), nullable=True)
    wow_server: Mapped[str] = mapped_column(String(24), nullable=True)
    wow_region: Mapped[str] = mapped_column(String(2), nullable=True)


class Users(Base):
    """Row Layout for the Users Table"""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('guilds.id'))
    name: Mapped[str] = mapped_column(String(40))
    wow_name: Mapped[str] = mapped_column(String(24), nullable=True)
    wow_server: Mapped[str] = mapped_column(String(24), nullable=True)
    wow_region: Mapped[str] = mapped_column(String(2), nullable=True)
