import pytest


@pytest.fixture
def mock_connect(mocker):
    mock = mocker.patch('wow_helper.db._connect').return_value = mocker.Mock()
    return mock


@pytest.fixture
def mock_session(mocker):
    mock = mocker.patch('wow_helper.db._create_session').return_value = mocker.Mock()
    return mock
