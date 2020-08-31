import pytest
from unittest.mock import MagicMock
from unittest import mock
from app import data_access_service, config_service
from app import app
from praw.models import Message
from praw.reddit import Reddit
import datetime


def test_is_too_old():
    conf = {'TODAY': datetime.date.today(), 'PERIOD': datetime.timedelta(days=10)}
    date = datetime.date.today()-datetime.timedelta(days=11)
    assert app._is_too_old(date, conf)
    date = date + datetime.timedelta(days=12)
    assert app._is_too_old(date, conf) == False


def test_is_user_subscribed():
    title = '[DISC] some title'
    conf = {'NEW_CHAPTER_CODE': '[DISC]'}
    user = { 'mangoes' : ['different title', 'some title']}
    assert app._is_user_subscribed(user, title, conf)
    title = 'abcd'
    assert app._is_user_subscribed(user, title, conf) == False


def test_append_mangoes_to_message():
    r = MagicMock()
    conf= {'TODAY': datetime.date.today(), "PERIOD": datetime.timedelta(days=10), "SUBREDDIT": "manga"}
    a = MagicMock()
    r.subreddit = MagicMock(return_value = a)
    a.new = MagicMock(return_value=[{"title": "a", "link": "b", "created_utc": datetime.date.today()}, {"title": "c", "link": "d", "created_utc": datetime.date.today()-datetime.timedelta(days=9)}])
    app._is_user_subscribed = MagicMock(return_value = False)
    message = "abc\n\n"
    assert app._append_mangoes_to_message(message, r, {}, conf) == message
    
    app._is_user_subscribed.return_value = True
    assert app._append_mangoes_to_message(message, r, {}, conf) == "abc\n\n* [a](b)\n* [c](d)\n"


def test_format_and_send_message():
    message = "test"
    r = MagicMock()
    a = MagicMock()
    r.redditor = MagicMock(return_value=a)
    a.message = MagicMock()
    conf = {"INSTRUCTIONS": "subscribe"}
    user = {"id": "1", "mangoes": ["mango1", "mango2"]}
    app._format_and_send_message(message, r, user, conf)
    r.redditor.assert_called_once_with("1")
    a.message.assert_called_once_with('YOUR MANGA SUBSCRIPTION', "test\n***\n# YOUR SUBSCRIPTIONS\n\n* mango1\n* mango2\n\n***\nsubscribe")


def test_update_users_subscriptions():
    app._append_mangoes_to_message = MagicMock(return_value="# Manga Updates:\n\n")
    app._format_and_send_message = MagicMock()
    r = MagicMock()
    assert app._update_users_subscriptions({}, r, {}) == None
    app._format_and_send_message.assert_not_called()

    message = "# Manga Updates:\n\nUpdates HERE\n"
    app._append_mangoes_to_message.return_value = message
    assert app._update_users_subscriptions({}, r, {}) == None
    app._format_and_send_message.assert_called_once_with(message, r, {}, {})


def test_update_subscriptions():
    data_access_service.fetch_subscriber_data = MagicMock()
    data_access_service.fetch_subscriber_data.return_value.users.return_value = ['a', 'b']
    app._update_users_subscriptions = MagicMock()
    r = MagicMock()
    #app.update_subscriptions(r, {'TIMEOUT': 5})
    #data_access_service.fetch_subscriber_data.assert_called_once() #_with(r, {'TIMEOUT': 5})
    #app._update_users_subscriptions.assert_called()