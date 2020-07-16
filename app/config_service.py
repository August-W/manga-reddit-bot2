from praw import Reddit
import os
import importlib
import datetime

TIMEOUT = 600
# HOW OFTEN SHOULD THIS RUN
PERIOD = 600000
TODAY = datetime.date.today()

NEW_CHAPTER_CODE = '[DISC]'
SUBREDDIT = 'manga'
DB_MESSAGE_SUBJECT = 'SO_CALLED_DB'
SUB_MESSAGE_SUBJECT = 'subscribe'
UNSUB_MESSAGE_SUBJECT = 'unsubscribe'
INSTRUCTIONS = '''Message me with the subject set to "subscribe" or "unsubscribe".\n
                    In the body of the message, list the manga you wish to subscribe to / unsubscribe from.\n
                    Separate each manga title in your list in a new line.\n
                    The title is not case-sensitive. '''

USER_AGENT = 'Manga Reddit Bot'
CLIENT_ID = ''
CLIENT_SECRET = ''
PASS = ''
USERNAME = ''


def _config_secrets(self) -> None:
    if importlib.util.find_spec('app.secret_properties') is not None:
        import app.secret_properties as secrets
        self.CLIENT_ID = secrets.CLIENT_ID
        self.CLIENT_SECRET = secrets.CLIENT_SECRET
        self.PASS = secrets.REDDIT_PASS
        self.USERNAME = secrets.REDDIT_USER
    else:
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        self.PASS = os.environ.get('REDDIT_PASS')
        self.USERNAME = os.environ.get('REDDIT_USER')


# SET UP THE REDDIT CONNECTION
def connect_to_reddit(self) -> Reddit:
    _config_secrets()
    return Reddit(user_agent=self.USER_AGENT,
                  client_id=self.CLIENT_ID,
                  client_secret=self.CLIENT_SECRET,
                  password=self.PASS,
                  username=self.USERNAME)

