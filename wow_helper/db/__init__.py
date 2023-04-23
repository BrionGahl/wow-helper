import sqlalchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy.engine import URL
from sqlalchemy import orm
import sys

from wow_helper import utils
from wow_helper import config
from wow_helper.db import models


logger = utils.get_logger(__name__)
url = URL.create(
        drivername='postgresql',
        username=config.db_user(),
        password=config.db_password(),
        host=config.db_host(),
        port=int(config.db_port()),
        database=config.db_name()
    )


def __connect() -> sqlalchemy.Connection:
    engine = sqlalchemy.create_engine(url)
    logger.info('Attempting to connect to supplied database...')
    try:
        connection = engine.connect()
    except DatabaseError as e:
        logger.error(e)
        logger.error('Unable to connect to database. Exiting...')
        sys.exit(2)
    logger.info('Successfully connected to database.')
    return connection


def __create_session(connection: sqlalchemy.Connection) -> orm.Session:
    logger.info("Creating session for transaction.")
    try:
        session = orm.Session(connection)
    except DatabaseError as e:
        logger.error(e)
        logger.error('Failed to create a session.')
        sys.exit(2)
    logger.info("Successfully created session.")
    return session


def ping() -> None:
    conn = __connect()
    conn.close()


def insert_guild(name: str, wow_name: str, wow_server: str) -> None:
    conn = __connect()
    session = __create_session(conn)

    new_guild = models.Guilds(name=name, wow_name=wow_name, wow_server=wow_server)
    session.add(new_guild)
    session.commit()

    session.close()
    conn.close()
    logger.info("Session complete.")


def insert_user(guild_id: int, name: str, wow_name: str, wow_server: str) -> None:
    conn = __connect()
    session = __create_session(conn)

    new_user = models.Users(guild_id=guild_id, name=name, wow_name=wow_name, wow_server=wow_server)
    session.add(new_user)
    session.commit()

    session.close()
    conn.close()
    logger.info("Session complete.")
