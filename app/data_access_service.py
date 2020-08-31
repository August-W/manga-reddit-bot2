from app import data_transform_util
from praw.models import Message
from praw.reddit import Reddit


# GETS MANGA TITLES BY SUBSCRIBER FROM LATEST MESSAGES
def _fetch_new_subscriber_messages(r: Reddit, conf: dict) -> list:
    new_subscriber_messages = []
    unread_items = []
    for message in r.inbox.unread(limit=None):
        if isinstance(message, Message) and message.author.name != conf['USERNAME']:
            new_subscriber_messages.append(message)
        unread_items.append(message)
    r.inbox.mark_read(unread_items)
    return new_subscriber_messages


# READS SUBSCRIBER DATA FROM BOTS SPECIAL MESSAGE
def _fetch_from_so_called_db(r: Reddit, conf: dict) -> list:
    for message in r.inbox.sent(limit=None):
        if(message.dest.name==conf['USERNAME']):
            return data_transform_util.init_db(message.body)
    return []


# UPDATES BOTS SPECIAL MESSAGE CONTAINING ALL SUBSCRIBER DATA
def _fetch_and_update_so_called_db(new_subscriber_messages: list, r: Reddit, conf: dict) -> list:
    db_data = _fetch_from_so_called_db(r, conf)
    db_data = data_transform_util.update(db_data, new_subscriber_messages, conf)
    writeable_db_data = data_transform_util.format_to_writeable_db_data(db_data)
    # RUN THIS PART ASYNCHRONOUSLY
    r.redditor(conf['USERNAME']).message(conf['DB_MESSAGE_SUBJECT'],
                                         writeable_db_data)
    print('fetch and update')
    print(db_data)
    return db_data


# GETS ALL SUBSCRIBER DATA
def fetch_subscriber_data(r: Reddit, conf: dict) -> list:
    new_subscriber_messages = _fetch_new_subscriber_messages(r, conf)
    return _fetch_and_update_so_called_db(new_subscriber_messages, r, conf)
