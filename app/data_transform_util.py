
# CONVERT DB_DATA TO STRING FOR SELF-MESSAGE
def format_to_writeable_db_data(db_data: list) -> str:
    writeable_data = ""
    for user in db_data:
        listed_mangoes = ""
        for manga in user['mangoes']:
            listed_mangoes += f"{manga}>(u*u)>"
        writeable_data = f"{writeable_data}{user['name']}:{listed_mangoes}\n"
    return writeable_data


# ADD OR REMOVE SUBSCRIPTION BASED ON MESSAGE
def update(db_data: list, messages: list, conf: dict) -> list:
    for message in messages:
        if message.subject.lower() == conf['UNSUB_MESSAGE_SUBJECT']:
            db_data = _update_unsubscribe(db_data, message)
        elif message.subject.lower() == conf['SUB_MESSAGE_SUBJECT']:
            db_data = _update_subscribe(db_data, message)
    db_data = _remove_users_with_no_subscriptions(db_data)
    return db_data


# DONT KEEP TRACK OF USERS WHEN THEY HAVE 0 SUBSCRIPTIONS
def _remove_users_with_no_subscriptions(db_data: list) -> list:
    remove_users = []
    for user in db_data:
        if user['mangoes'] is None or len(user['mangoes']) == 0:
            remove_users.append(user)
    db_data = [x for x in db_data if x not in remove_users]
    return db_data


# ADD NEWLY SUBSCRIBED MANGA TO USER OR NEW USER
def _update_subscribe(db_data: list, message: dict) -> list:
    lines = message.body.splitlines()
    for user in db_data:
        if user['name'] == message.author.name:
            for line in lines:
                if line not in user['mangoes']:
                    user['mangoes'].append(line)
            return db_data
    db_data.append({'name': message.author.name, 'mangoes': lines})
    return db_data

# REMOVE NEWLY UNSUBSCRIBED MANGA FROM USER
def _update_unsubscribe(db_data: list, message: dict) -> list:
    print("unsubscribing")
    for user in db_data:
        if user['name'] == message.author.name:
            lines = message.body.splitlines()
            user['mangoes'] = [x for x in user['mangoes'] if x not in lines ]
            break
    return db_data


# INIT DB_DATA BASED ON SELF-MESSAGE
def init_db(message: str) -> list:
    db_data = []
    lines = message.splitlines()
    for line in lines:
        var_break = line.find(':')
        db_data.append({'name': line[:var_break], 'mangoes': line[var_break+1:].split('>(u*u)>')[:-1]})
    return db_data
