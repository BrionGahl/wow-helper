import os
from os.path import join, dirname
import sys
from dotenv import load_dotenv

from wow_helper import utils

logger = utils.get_logger(__name__)
load_dotenv(join(dirname(__file__), '../.env'))


if os.getenv('CONFIG_VERSION') != utils.config_version():
    if os.path.isfile('../.env'):
        logger.error('Missing environment variables.')
        sys.exit(1)
    logger.error('Unable to find required environment variables. Does your ".env" file exist?')
    sys.exit(1)


def bot_prefix() -> str:
    return os.environ.get("BOT_PREFIX")


def bot_token() -> str:
    return os.environ.get("BOT_TOKEN")


def wl_client_id() -> str:
    return os.environ.get("WL_CLIENT_ID")


def wl_client_secret() -> str:
    return os.environ.get("WL_CLIENT_SECRET")


def be_client_id() -> str:
    return os.environ.get("BE_CLIENT_ID")


def be_client_secret() -> str:
    return os.environ.get("BE_CLIENT_SECRET")


def db_host() -> str:
    return os.environ.get("DB_HOST")


def db_port() -> str:
    return os.environ.get("DB_PORT")


def db_name() -> str:
    return os.environ.get("DB_NAME")


def db_user() -> str:
    return os.environ.get("DB_USER")


def db_password() -> str:
    return os.environ.get("DB_PASS")
