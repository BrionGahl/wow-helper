import os
from os.path import join, dirname
import sys
from dotenv import load_dotenv

from wow_helper.utils import config_version

load_dotenv(join(dirname(__file__), '../.env'))

if os.getenv('CONFIG_VERSION') != config_version():
    if os.path.isfile('../.env'):
        print('ERROR: Missing environment variables.')
        sys.exit(2)
    print('ERROR: Unable to find required environment variables. Does your ".env" file exist?')
    sys.exit(2)


def bot_prefix() -> str:
    return os.environ.get("BOT_PREFIX")


def bot_token() -> str:
    return os.environ.get("BOT_TOKEN")


def wl_client_id() -> str:
    return os.environ.get("WL_CLIENT_ID")


def wl_client_secret() -> str:
    return os.environ.get("WL_CLIENT_SECRET")
