import pytest
from unittest.mock import MagicMock
from app import data_transform_util, config_service

def test_format_to_writeable_db_data():
    raw_data = {'users': [{'id': 1, 'mangoes': ['test_manga', 'test_manga2']},
                          {'id': 2, 'mangoes': ['test_mango2']}]}
    writeable_data = '1:test_manga>(u*u)>test_manga2>(u*u)\n2:test_mango2>(*u*)>\n'
    assert data_transform_util._format_to_writeable_db_data(raw_data) == writeable_data


def test_update():
    config_service.SUB_MESSAGE_SUBJECT = 'subtest'
    config_service.UNSUB_MESSAGE_SUBJECT = 'unsubtest'
    message1 = {'subject': 'SUBTEST'}
    message2 = {'subject': 'uNSUbTest'}
    message3 = {'subject': 'ERROR'}
    messages = [message1, message2, message3]
    result = ['result']
    data_transform_util._update_unsubscribe = MagicMock()
    data_transform_util._update_subscribe = MagicMock()
    data_transform_util._remove_users_with_no_subscriptions = MagicMock(return_value=result)
    assert data_transform_util._update([], messages) == result
    data_transform_util._update_unsubscribe.assert_called_once_with(message2)
    data_transform_util._update_subscribe.assert_called_once_with(message1)


def test_remove_users_with_no_subscriptions():
    db_data = [{'mangoes': None}, {'mangoes': ['m1', 'm2']}, {'mangoes': []}]
    assert data_transform_util._remove_users_with_no_subscriptions(db_data) == {'mangoes': ['m1', 'm2']}


def test_update_subscribe():
    db_data = [{'id': 1, 'mangoes': ['m0']}, {'id': 2, 'mangoes': ['m1']}]
    message = {'author': {'id': 1}, 'body': 'm1\nm2\nm3\n'}
    message2 = {'author': {'id': 2}, 'body': 'm1\n'}
    result = data_transform_util._update_subscribe(db_data, message)
    result2 = data_transform_util._update_subscribe(db_data, message2)
    assert result == [{'id': 1, 'mangoes': ['m0,m1,m2,m3']}, {'id': 2, 'mangoes': ['m1']}]
    assert result2 == [{'id': 1, 'mangoes': ['m0']}, {'id': 2, 'mangoes': ['m1\nm1\n']}]


def test_update_unsubscribe():
    db_data = [{'id': 1, 'mangoes': ['m0','m1']}, {'id': 2, 'mangoes': ['m1']}]
    message1 = {'author': {'id': 1}, 'body': 'm1\n'}
    message2 = {'author': {'id': 2}, 'body': 'm2\n'}
    result = data_transform_util._update_unsubscribe(db_data, message1)
    result2 = data_transform_util._update_unsubscribe(db_data, message2)
    assert result == [{'id': 1, 'mangoes': ['m0']}, {'id': 2, 'mangoes': ['m1']}]
    assert result2 == [{'id': 1, 'mangoes': ['m0', 'm1']}, {'id': 2, 'mangoes': ['m1']}]


def test_init_db():
    message = "1:test_manga>(u*u)>test_manga2>(u*u)\n2:test_mango2>(*u*)\n"
    assert init_db(message) == {'users': [{'id': 1, 'mangoes': ['test_manga', 'test_manga2']},
                                          {'id': 2, 'mangoes': ['test_mango2']}]}


def test_update_and_format_to_writeable_db_data():
    data_transform_util._update = MagicMock()
    result = ['result']
    data_transform_util._format_to_writeable_db_data = MagicMock(return_value=result)
    assert data_transform_util.test_update_and_format_to_writeable_db_data([], ['a'])
    data_transform_util._update.assert_called_once_with([], ['a'])
    data_transform_util._format_to_writeable_db_data.assert_called_once_with([])
