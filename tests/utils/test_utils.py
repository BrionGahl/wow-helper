import datetime
from logging import Logger

from wow_helper import utils


def test_version():
    assert utils.version() == 'v0.0.1'


def test_config_version():
    assert utils.config_version() == '0.1'


def test_time():
    expected = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert expected == utils.time()


def test_get_logger():
    logger = utils.get_logger('test')
    assert isinstance(logger, Logger)
