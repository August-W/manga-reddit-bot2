from app import config_service


def _format_to_writeable_db_data(db_data: list) -> str:
    writeable_data = ""
    for user in db_data.users:
        listed_mangoes = ""
        for manga in user.mangoes:
            listed_mangoes = f"{manga}>(u*u)>"
        writeable_data = f"{writeable_data}{user.id}:{listed_mangoes}\n"
    return writeable_data


# Add or remove subscription based on message
def _update(db_data: list, messages: list) -> list:
    for message in messages:
        if message.subject.lower() == config_service.UNSUB_MESSAGE_SUBJECT:
            db_data = _update_unsubscribe(db_data, message)
        elif message.subject.lower() == config_service.SUB_MESSAGE_SUBJECT:
            db_data = _update_subscribe(db_data, message)

    db_data = _remove_users_with_no_subscriptions(db_data)
    return db_data


def _remove_users_with_no_subscriptions(db_data: list) -> list:
    remove_users = []
    for user in db_data:
        if len(user.mangoes) == 0:
            remove_users.append(user)
    db_data.remove(remove_users)
    return db_data


def _update_subscribe(db_data: list, message: dict) -> list:
    for user in db_data:
        if user.id == message.author.id:
            lines = message.body.splitlines()
            for line in lines:
                user.mangoes.append(line)
    return db_data


def _update_unsubscribe(db_data: list, message: dict) -> list:
    for user in db_data:
        if user.id == message.author.id:
            lines = message.body.splitlines()
            for line in lines:
                user.mangoes.remove(line)
    return db_data


# init based on special message
def init_db(message: str) -> list:
    db_data = []
    lines = message.splitlines()
    for line in lines:
        var_break = line.find(':')
        db_data.append({'id': line[:var_break], 'mangoes': line[var_break:].split('>(u*u)>')})
    return db_data


def update_and_format_to_writeable_db_data(db_data: list, messages: list) -> list:
    db_data = _update(db_data, messages)
    db_data = _format_to_writeable_db_data(db_data)
    return db_data
