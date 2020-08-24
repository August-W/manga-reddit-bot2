import pytest
from unittest.mock import MagicMock
from app import config_service, data_access_service, data_transform_util
import importlib
import itertools
import os
from praw import Reddit
from praw.models import Message


def test_fetch_new_subscriber_messages():
    r = MagicMock()
    mess = Message(r, {})
    mess.author = MagicMock(return_value='b')
    r.inbox.unread.return_value = ['a', mess]
    assert data_access_service._fetch_new_subscriber_messages(r, {'USERNAME': 'b'}) == [mess]
    r.inbox.mark_read.assert_called_once_with(['a', mess])


def test_fetch_from_so_called_db():
    data_transform_util.init_db = MagicMock(return_value='result')
    reddit = MagicMock()
    reddit.inbox.sent.return_value = itertools.cycle('test')
    assert data_access_service._fetch_from_so_called_db(reddit) == 'result'

    reddit.inbox.sent.return_value = []
    assert data_access_service._fetch_from_so_called_db(reddit) == []


def test_fetch_and_update_so_called_db():
    old_result = ['old_result']
    result = ['result']
    data_access_service._fetch_from_so_called_db = MagicMock(return_value=old_result)
    data_transform_util.update_and_format_to_writeable_db_data = MagicMock(return_value=result)
    r = MagicMock()
    redditor = MagicMock()
    r.redditor.return_value = redditor
    mock_conf = {'USERNAME': 'a', 'DB_MESSAGE_SUBJECT': 'b'}
    assert data_access_service._fetch_and_update_so_called_db(['x'], r, mock_conf) == result
    data_access_service._fetch_from_so_called_db.assert_called_once()
    data_transform_util.update_and_format_to_writeable_db_data.assert_called_once_with(old_result, ['x'], mock_conf)
    r.redditor.assert_called_once_with('a')
    redditor.message.assert_called_once_with('b', result)


def test_fetch_subscriber_data():
    data_access_service._fetch_new_subscriber_messages = MagicMock()
    data_access_service._fetch_and_update_so_called_db = MagicMock(return_value='result')
    assert data_access_service.fetch_subscriber_data(MagicMock(), {}) == 'result'
    data_access_service._fetch_new_subscriber_messages.assert_called_once()