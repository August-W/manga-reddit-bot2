import asyncio
from app import data_access_service
from app import config_service
from praw.reddit import Reddit


# OUTSIDE OF PERIODIC SCOPE
def _is_too_old(date) -> bool:
    return date + config_service.PERIOD < config_service.TODAY


def _is_user_subscribed(user: dict, title: str) -> bool:
    if config_service.NEW_CHAPTER_CODE in title:
        for manga in user.mangoes:
            if manga in title:
                return True
    return False


async def _update_users_subscriptions(user: dict, r: Reddit) -> None:
    message = "# Manga Updates:\n\n"
    # LIMIT BY DATE/TIME
    message = await _append_mangoes_to_message(message, r, user)
    if message != "# Manga Updates:\n\n":
        await _format_and_send_message(message, r, user)
    return None


async def _append_mangoes_to_message(message: str, r: Reddit, user: dict) -> str:
    for submission in r.subreddit(config_service.SUBREDDIT).new(limit=None):
        if _is_too_old(submission.created_utc):
            break
        elif _is_user_subscribed(user, submission.title):
            message = f"{message}* [{submission.title}]({submission.link})\n"
    return message


async def _format_and_send_message(message: str, r: Reddit, user: dict) -> None:
    message = f"{message}\n***\n# YOUR SUBSCRIPTIONS\n\n"
    for subscription in user.mangues:
        message = f"{message}* {subscription}\n"
    message = f"{message}\n***\n{config_service.INSTRUCTIONS}"
    r.redditor(user.id).message('YOUR MANGA SUBSCRIPTION', message)


async def update_subscriptions(r: Reddit) -> list:
    subscriber_data = data_access_service.fetch_subscriber_data(r)
    update_tasks = [asyncio.create_task(_update_users_subscriptions(user, r)) for user in subscriber_data.users]
    return await asyncio.wait(asyncio.gather(*update_tasks), timeout=config_service.TIMEOUT)

