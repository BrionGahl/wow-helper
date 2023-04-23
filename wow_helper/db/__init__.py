import sqlalchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy.engine import URL
import sys

from wow_helper import utils
from wow_helper import config


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


def ping():
    conn = __connect()
    conn.close()
