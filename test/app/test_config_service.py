import pytest
from unittest.mock import MagicMock
from app import config_service
import importlib
import os
from praw import Reddit


def test_config_secrets():
    importlib.util.find_spec = MagicMock()
    os.environ.get = MagicMock(return_value='good enough')
    config_service._config_secrets()
    os.environ.get.assert_not_called()
    importlib.util.find_spec = MagicMock(return_value=None)
    config_service._config_secrets()
    assert config_service.CLIENT_ID = 'good enough'
    assert config_service.CLIENT_SECRET = 'good enough'
    assert config_service.REDDIT_PASS = 'good enough'
    assert config_service.REDDIT_USER = 'good enough'


def test_connect_to_reddit():
    Reddit = MagicMock()
    config_service._config_secrets = MagicMock()
    config_service.connect_to_reddit()
    config_service._config_secrets.assert_called_once()
    config_service.Reddit.assert_called_once_with(user_agent='Manga Reddit Bot',
                                                           client_id='', client_secret='',
                                                           password='', username='')
