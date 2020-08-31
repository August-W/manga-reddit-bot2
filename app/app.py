import asyncio
import datetime
from app import data_access_service
from praw.reddit import Reddit


# OUTSIDE OF PERIODIC SCOPE
def _is_too_old(date, conf: dict) -> bool:
    return date + conf["PERIOD"] < conf["TODAY"]


def _is_user_subscribed(user: dict, title: str, conf: dict) -> bool:
    if conf["NEW_CHAPTER_CODE"] in title:
        for manga in user["mangoes"]:
            if manga.lower() in title.lower():
                return True
    return False


async def _update_users_subscriptions(user: dict, r: Reddit, conf: dict) -> None:
    message = "# Manga Updates:\n\n"
    await asyncio.sleep(1)
    message = _append_mangoes_to_message(message, r, user, conf)
    if message != "# Manga Updates:\n\n":
        _format_and_send_message(message, r, user, conf)
    return None


def _append_mangoes_to_message(message: str, r: Reddit, user: dict, conf: dict) -> str:
    for submission in r.subreddit(conf["SUBREDDIT"]).new(limit=None):
        if _is_too_old(datetime.date.fromtimestamp(submission.created_utc), conf):
            print("IN TOO OLD")
            break
        elif _is_user_subscribed(user, submission.title, conf):
            print("IN RIGHT AGE")
            message = f"{message}* [{submission.title}]({submission.url})\n"
    return message


def _format_and_send_message(message: str, r: Reddit, user: dict, conf: dict) -> None:
    message = f"{message}\n***\n# YOUR SUBSCRIPTIONS\n\n"
    for subscription in user["mangoes"]:
        message = f"{message}* {subscription}\n"
    message = f"{message}\n***\n{conf['INSTRUCTIONS']}"
    r.redditor(user["name"]).message('YOUR MANGA SUBSCRIPTION', message)


def update_subscriptions(r: Reddit, conf: dict):
    subscriber_data = data_access_service.fetch_subscriber_data(r, conf)
    update_tasks = [_update_users_subscriptions(user, r, conf) for user in subscriber_data]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*update_tasks))
    loop.close()

