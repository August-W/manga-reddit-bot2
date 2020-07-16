from app import data_transform_util, config_service
from praw.models import Message
from praw.reddit import Reddit


# GETS MANGA TITLES BY SUBSCRIBER FROM LATEST MESSAGES
def _fetch_new_subscriber_messages(r: Reddit) -> list:
    new_subscriber_messages = []
    unread_items = []
    for message in r.inbox.unread(limit=None):
        if isinstance(message, Message) and message.author != config_service.REDDIT_USER:
            new_subscriber_messages.append(message)
        unread_items.append(message)
    r.inbox.mark_read(unread_items)
    return new_subscriber_messages


# READS SUBSCRIBER DATA FROM BOTS SPECIAL MESSAGE
def _fetch_from_so_called_db(r: Reddit) -> list:
    for message in r.inbox.sent(limit=1):
        return data_transform_util.init_db(message)
    return []


# UPDATES BOTS SPECIAL MESSAGE CONTAINING ALL SUBSCRIBER DATA
def _fetch_and_update_so_called_db(new_subscriber_messages: list, r: Reddit) -> list:
    db_data = _fetch_from_so_called_db()
    db_data = data_transform_util.update_and_format_to_writeable_db_data(db_data, new_subscriber_messages)
    # RUN THIS PART ASYNCHRONOUSLY
    r.redditor(config_service.REDDIT_USER).message(config_service.DB_MESSAGE_SUBJECT,
                                                   db_data)
    return db_data


# GETS ALL SUBSCRIBER DATA
def fetch_subscriber_data(r: Reddit) -> list:
    new_subscriber_messages = _fetch_new_subscriber_messages(r)
    return _fetch_and_update_so_called_db(new_subscriber_messages, r)
