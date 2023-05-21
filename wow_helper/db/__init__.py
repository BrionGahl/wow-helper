from typing import Union
import sys
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.exc import DatabaseError, DataError, OperationalError
from sqlalchemy.engine import URL

from wow_helper import utils, config
from wow_helper.db import models

"""
Functions used in creating connections and sessions to the Postgres Database, as well as transactions and CRUD
operations.
"""

logger = utils.get_logger(__name__)
url = URL.create(
        drivername='postgresql',
        username=config.db_user(),
        password=config.db_password(),
        host=config.db_host(),
        port=int(config.db_port()),
        database=config.db_name()
    )
engine = sqlalchemy.create_engine(url)


def _connect() -> sqlalchemy.Connection:
    logger.info('Attempting to connect to database...')
    try:
        connection = engine.connect()
    except DatabaseError as e:
        logger.error(e)
        logger.error('Unable to connect to database. Exiting...')
        sys.exit(1)
    logger.info('Successfully connected to database.')
    return connection


def _create_session(connection: sqlalchemy.Connection) -> orm.Session:
    logger.info('Creating session for transaction.')
    try:
        session = orm.Session(connection)
    except DatabaseError as e:
        logger.error(e)
        logger.error('Failed to create a session.')
        sys.exit(1)
    logger.info('Successfully created session.')
    return session


def instantiate_tables() -> None:
    try:
        models.Guilds.__table__.create(bind=engine, checkfirst=True)
        models.Users.__table__.create(bind=engine, checkfirst=True)
    except OperationalError as e:
        logger.error(e)
        logger.error('Failed to connect to the database.')
        sys.exit(1)
    logger.info('Database verified and configured.')


def get_guild_information(g_id: int) -> Union[tuple[str, str, str], None]:
    conn = _connect()
    session = _create_session(conn)

    retrieved = session.query(models.Guilds).get(g_id)
    if retrieved is None:
        logger.error('Failed to find guild information.}')
        return

    return retrieved.wow_name.strip(), retrieved.wow_server.strip(), retrieved.wow_region.strip()


def insert_guild(g_id: int, name: str) -> bool:
    conn = _connect()
    session = _create_session(conn)

    added = False

    retrieved = session.query(models.Guilds).get(g_id)
    if retrieved is None:
        added = True
        logger.info('New Discord guild detected, adding it to the database.')
        new_guild = models.Guilds(id=g_id, name=name, wow_name=None, wow_server=None, wow_region=None)
        session.add(new_guild)
        session.commit()

    session.close()
    conn.close()
    logger.info('Transaction complete.')
    return added


def update_guild(g_id: int, name: Union[str, None] = None, wow_name: Union[str, None] = None, wow_server: Union[str, None] = None, wow_region: Union[str, None] = None) -> models.Guilds:
    conn = _connect()
    session = _create_session(conn)

    logger.info('Updating information on current guild.')

    retrieved = session.query(models.Guilds).get(g_id)

    retrieved.name = name if name else retrieved.name
    retrieved.wow_name = wow_name if wow_name else retrieved.wow_name
    retrieved.wow_server = wow_server if wow_server else retrieved.wow_server
    retrieved.wow_region = wow_region if wow_region else retrieved.wow_region

    session.commit()

    session.close()
    conn.close()
    logger.info('Transaction complete.')

    return retrieved


def delete_guild(g_id: int) -> bool:
    conn = _connect()
    session = _create_session(conn)

    logger.info(f'Deleting guild under ID {g_id}.')
    retrieved = session.query(models.Guilds).get(g_id)

    if retrieved is None:
        logger.error(f'Failed to delete guild under ID {g_id}, no guild found.')
        return False

    session.delete(retrieved)
    session.commit()

    session.close()
    conn.close()
    logger.info('Transaction Complete.')
    return True


def get_user_information(u_id: int) -> Union[tuple[str, str, str], None]:
    conn = _connect()
    session = _create_session(conn)

    retrieved = session.query(models.Users).get(u_id)
    if retrieved is None:
        logger.error('Failed to find user information.}')
        return

    return retrieved.wow_name.strip(), retrieved.wow_server.strip(), retrieved.wow_region.strip()


def insert_or_update_user(u_id: int, g_id: int, name: Union[str, None] = None, wow_name: Union[str, None] = None, wow_server: Union[str, None] = None, wow_region: Union[str, None] = None) -> models.Users:
    conn = _connect()
    session = _create_session(conn)

    retrieved = session.query(models.Users).get(u_id)
    if retrieved is None:
        logger.info('New Discord guild member detected, adding it to the database.')

        retrieved = models.Users(id=u_id, guild_id=g_id, name=name, wow_name=wow_name, wow_server=wow_server, wow_region=wow_region)
        session.add(retrieved)
    else:
        logger.info('Updating information on current user.')

        retrieved.guild_id = g_id
        retrieved.name = name if name else retrieved.name
        retrieved.wow_name = wow_name if wow_name else retrieved.wow_name
        retrieved.wow_server = wow_server if wow_server else retrieved.wow_server
        retrieved.wow_region = wow_region if wow_region else retrieved.wow_region

    session.commit()

    session.close()
    conn.close()
    logger.info('Transaction Complete.')
    return retrieved


def delete_user(u_id: int) -> bool:
    conn = _connect()
    session = _create_session(conn)

    logger.info(f'Deleting user under ID {u_id}.')
    retrieved = session.query(models.Users).get(u_id)

    if retrieved is None:
        logger.error(f'Failed to delete user under ID {u_id}, no user found.')
        return False

    session.delete(retrieved)
    session.commit()

    session.close()
    conn.close()
    logger.info('Transaction Complete.')
    return True
