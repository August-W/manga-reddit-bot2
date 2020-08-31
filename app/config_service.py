from praw import Reddit
import os
import importlib
import datetime


def _init_config() -> dict:
    return {
        'PERIOD': datetime.timedelta(days=3),
        'TODAY': datetime.date.today(),

        'NEW_CHAPTER_CODE': '[DISC]',
        'SUBREDDIT': 'manga',
        'DB_MESSAGE_SUBJECT': 'SO_CALLED_DB',
        'SUB_MESSAGE_SUBJECT': 'subscribe',
        'UNSUB_MESSAGE_SUBJECT': 'unsubscribe',
        'INSTRUCTIONS': 'Message me with the subject set to "subscribe" or "unsubscribe".\n'+
                            'In the body of the message, list the manga you wish to subscribe to / unsubscribe from.\n'+
                            'Separate each manga title in your list in a new line.\n'+
                            'The title is not case-sensitive.',

        'USER_AGENT': 'Manga Subscriber Bot',
        'CLIENT_ID': '',
        'CLIENT_SECRET': '',
        'PASS': '',
        'USERNAME': ''
    }


def _config_secrets() -> dict:
    conf = _init_config()
    if importlib.util.find_spec('app.secret_properties') is not None:
        import app.secret_properties as secrets
        conf['CLIENT_ID'] = secrets.CLIENT_ID
        conf['CLIENT_SECRET'] = secrets.CLIENT_SECRET
        conf['PASS'] = secrets.REDDIT_PASS
        conf['USERNAME'] = secrets.REDDIT_USER
    else:
        conf['CLIENT_ID'] = os.environ.get('CLIENT_ID')
        conf['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')
        conf['PASS'] = os.environ.get('REDDIT_PASS')
        conf['USERNAME'] = os.environ.get('REDDIT_USER')
    return conf


# SET UP THE REDDIT CONNECTION
def connect_to_reddit() -> (Reddit, dict):
    conf = _config_secrets()
    return Reddit(user_agent=conf["USER_AGENT"],
                  client_id=conf["CLIENT_ID"],
                  client_secret=conf["CLIENT_SECRET"],
                  password=conf["PASS"],
                  username=conf["USERNAME"]), conf

