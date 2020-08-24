import pytest
from unittest.mock import MagicMock
from app import data_access_service, config_service
import app
from praw.models import Message
from praw.reddit import Reddit
import datetime


def test_is_too_old():
    date = datetime.date.today()-config_service.PERIOD-1
    assert app._is_too_old(date)
    date = date + 2
    assert app._is_too_old(date) == False


def test_is_user_subscribed():
    title = '[DISC] some title'
    user = { 'mangoes' ['different title', 'some title']}
    assert app._is_user_subscribed(user, title)
    title = 'abcd'
    assert app._is_user_subscribed(user, title) == False


def test_update_users_subscriptions():
    app._append_mangoes_to_message = MagicMock(return_value="# Manga Updates:\n\n")
    app._format_and_send_message = MagicMock()
    r = MagicMock()
    assert app._update_users_subscriptions({}, r) == None
    app._format_and_send_message.assert_not_called()

    message = "# Manga Updates:\n\nUpdates HERE\n"
    app._append_mangoes_to_message.return_value = message
    assert app._update_users_subscriptions({}, r) == None
    app._format_and_send_message.assert_called_once_with(message, r, {})


def test_append_mangoes_to_message():
    r = MagicMock()
    r.subreddit.new.return_value = [{"title": "a", "link": "b", "created_utc": datetime.date.today()}, {"title": "c", "link": "d", "created_utc": datetime.date.today()-config_service.PERIOD-1}]
    r._is_user_subscribed.return_value = False
    message = "abc\n\n"
    assert app._append_mangoes_to_message(message, r, {}) == message
    
    r._is_user_subscribed.return_value = True
    assert app._append_mangoes_to_message(message, r, {}) == "abc\n\n[a](b)\n"


def test_format_and_send_message():




def test_update_subscriptions():
    data_access_service.fetch_subscriber_data = MagicMock()
    data_access_service.fetch_subscriber_data.return_value.users.return_value = ['a', 'b']
    app._update_users_subscriptions = MagicMock()
    r = MagicMock()
    app.update_subscriptions(r)
    data_access_service.fetch_subscriber_data.assert_called_once_with(r)
    app._update_users_subscriptions.assert_called()