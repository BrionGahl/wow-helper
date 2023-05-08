import pytest
from sqlalchemy.exc import DatabaseError, DataError, OperationalError

from wow_helper import db
from wow_helper.db import models


def test_instantiate_tables_on_success(mocker):
    mocker.patch("wow_helper.db.models.Guilds.__table__.create")
    mocker.patch("wow_helper.db.models.Users.__table__.create")

    assert db.instantiate_tables() is None


def test_instantiate_tables_on_failure(mocker):
    mocker.patch('wow_helper.db.models.Guilds.__table__.create', side_effect=OperationalError('mock', None, Exception()))

    with pytest.raises(SystemExit) as wrapped_exit:
        db.instantiate_tables()
    assert wrapped_exit.type == SystemExit
    assert wrapped_exit.value.code == 1


def test_get_guild_information_on_success(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = models.Guilds(id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')
    guild_info = db.get_guild_information(1)

    assert guild_info == ('mocked_name', 'mocked_server', 'us')


def test_get_guild_information_on_failure(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None

    assert db.get_guild_information(1) is None


def test_insert_guild_does_exists(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = models.Guilds(id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')

    assert db.insert_guild(1, 'mocked_guild_name') is False


def test_insert_guild_does_not_exist(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None

    assert db.insert_guild(1, 'mocked_guild_name') is True


def test_update_guild(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = models.Guilds(id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')
    expected = models.Guilds(id=1, name='mock_name', wow_name='mock_name', wow_server='mock_name', wow_region='us')
    actual = db.update_guild(1, name='mock_name', wow_name='mock_name', wow_server='mock_name')

    assert actual.id == expected.id
    assert actual.name == expected.name
    assert actual.wow_name == expected.wow_name
    assert actual.wow_server == expected.wow_server


def test_delete_guild_on_success(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = models.Guilds(id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')

    assert db.delete_guild(1) is True


def test_delete_guild_on_failure(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None

    assert db.delete_guild(1) is False


def test_get_user_information_on_success(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = db.models.Users(id=1, guild_id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')
    user_info = db.get_user_information(1)

    assert user_info == ('mocked_name', 'mocked_server', 'us')


def test_get_user_information_on_failure(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None

    assert db.get_user_information(1) is None


def test_insert_or_update_user_on_insert(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None
    expected = models.Users(id=1, guild_id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')
    actual = db.insert_or_update_user(1, 1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')

    assert actual.id == expected.id
    assert actual.guild_id == expected.guild_id
    assert actual.name == expected.name
    assert actual.wow_name == expected.wow_name
    assert actual.wow_server == expected.wow_server


def test_insert_or_update_user_on_update(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = models.Users(id=1, guild_id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')
    expected = models.Users(id=1, guild_id=1, name='new_name', wow_name='new_wow_name', wow_server='mocked_server', wow_region='us')
    actual = db.insert_or_update_user(1, 1, name='new_name', wow_name='new_wow_name', wow_server='mocked_server', wow_region='us')

    assert actual.id == expected.id
    assert actual.guild_id == expected.guild_id
    assert actual.name == expected.name
    assert actual.wow_name == expected.wow_name
    assert actual.wow_server == expected.wow_server


def test_delete_user_on_success(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = db.models.Users(id=1, guild_id=1, name='mocked_guild_name', wow_name='mocked_name', wow_server='mocked_server', wow_region='us')

    assert db.delete_user(1) is True


def test_delete_user_on_failure(mock_connect, mock_session):
    mock_session.query.return_value.get.return_value = None

    assert db.delete_user(1) is False
