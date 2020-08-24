import pytest
from unittest import mock
from unittest.mock import MagicMock
from app import config_service
import importlib
import os
from praw import Reddit


@mock.patch.dict(os.environ, {"CLIENT_ID": "a", "CLIENT_SECRET": "b", "REDDIT_PASS": "c", "REDDIT_USER": "d"})
def test_config_secrets():
    importlib.util.find_spec = MagicMock(return_value=None)
    result = config_service._config_secrets()
    assert result['CLIENT_ID'] == 'a'
    assert result['CLIENT_SECRET'] == 'b'
    assert result['PASS'] == 'c'
    assert result['USERNAME'] == 'd'


def test_connect_to_reddit():
    Reddit.__init__ = MagicMock(return_value=None)
    config_service._config_secrets = MagicMock()
    result_r, result_conf = config_service.connect_to_reddit()
    config_service._config_secrets.assert_called_once()
    config_service.Reddit.__init__.assert_called_once()
