import datetime
from praw.reddit import Reddit

from app import data_access_service


# OUTSIDE OF PERIODIC SCOPE
def _is_too_old(date, conf: dict) -> bool:
    return date + conf["PERIOD"] < conf["TODAY"]


# IS THIS USER CURRENTLY SUBSCRIBED TO THIS MANGA
def _is_user_subscribed(user: dict, title: str, conf: dict) -> bool:
    if conf["NEW_CHAPTER_CODE"] in title:
        for manga in user["mangoes"]:
            if manga.lower() in title.lower():
                return True
    return False


# GENERATE MESSAGE WITH SUBSCRIBED MANGA UPDATES
def _update_users_subscriptions(user: dict, r: Reddit, conf: dict, all_submissions) -> None:
    message = "# Manga Updates:\n\n"
    message = _append_mangoes_to_message(message, r, user, conf, all_submissions)
    if message != "# Manga Updates:\n\n":
        _format_and_send_message(message, r, user, conf)
    return None


# ONLY INCLUDE MANGA UPDATES SINCE THE LAST TIME THE BOT RAN
def _append_mangoes_to_message(message: str, r: Reddit, user: dict, conf: dict, all_submissions) -> str:
    for submission in all_submissions:
        if _is_too_old(datetime.date.fromtimestamp(submission.created_utc), conf):
            break
        elif _is_user_subscribed(user, submission.title, conf):
            message = f"{message}* [{submission.title}]({submission.url})\n"
    return message


# GENERATE MESSAGE FOR SUBSCRIBER
def _format_and_send_message(message: str, r: Reddit, user: dict, conf: dict) -> None:
    message = f"{message}\n***\n# YOUR SUBSCRIPTIONS\n\n"
    for subscription in user["mangoes"]:
        message = f"{message}* {subscription}\n"
    message = f"{message}\n***\n{conf['INSTRUCTIONS']}"
    r.redditor(user["name"]).message('YOUR MANGA SUBSCRIPTION', message)
    return None


# UPDATE SUBSCRIPTIONS FOR EACH USER
def update_subscriptions(r: Reddit, conf: dict) -> None:
    subscriber_data = data_access_service.fetch_subscriber_data(r, conf)
    all_submissions = r.subreddit(conf["SUBREDDIT"]).new(limit=None)
    for user in subscriber_data:
        _update_users_subscriptions(user, r, conf, all_submissions)
    return None

