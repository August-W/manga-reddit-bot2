import pytest
from unittest.mock import MagicMock
from app import config_service, data_access_service, data_transform_util
import importlib
import os
from praw import Reddit
from praw.models import Message


def test_fetch_new_subscriber_messages():
    r = MagicMock()
    mess = Mressage()
    r.inbox.unread.return_value = ['a', mess]
    assert data_access_service._fetch_new_subscriber_messages(r) == [mess]
    r.inbox.mark_read.assert_called_once_with(['a', mess])


def test_fetch_from_so_called_db():
    data_transform_util = MagicMock()
    data_transform_util.init_db.return_value = 'result'
    reddit = MagicMock()
    reddit.inbox.sent.return_value = ['test']
    assert data_access_service._fetch_from_so_called_db(reddit) == 'result'

    reddit.inbox.sent.return_value = None
    assert data_access_service._fetch_from_so_called_db(reddit) == []


def test_fetch_and_update_so_called_db():
    result = ['result']
    data_access_service._fetch_from_so_called_db = MagicMock(return_value=result)
    data_transform_util.update_and_format_to_writeable_db_data = MagicMock()
    r = MagicMock()
    redditor = MagicMock()
    r.redditor.return_value = redditor
    assert data_access_service._fetch_and_update_so_called_db(['x'], r) == result
    data_access_service._fetch_from_so_called_db.assert_called_once()
    data_transform_util.update_and_format_to_writeable_db_data.assert_called_once_with(result, ['x'])
    r.redditor.assert_called_once_with(config_service.REDDIT_USER)
    redditor.message.assert_called_once_with(config_service.DB_MESSAGE_SUBJECT, result)


def test_fetch_subscriber_data():
    data_access_service._fetch_new_subscriber_messages = MagicMock()
    data_access_service._fetch_and_update_so_called_db = MagicMock(return_value='result')
    assert data_access_service.fetch_subscriber_data(MagicMock())