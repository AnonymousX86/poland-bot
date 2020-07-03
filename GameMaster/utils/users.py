# -*- coding: utf-8 -*-
def check_mention(arg: str) -> int:
    if len(arg) == 21:
        arg = arg[2:-1]

    elif len(arg) == 22:
        arg = arg[3:-1]

    if len(arg) == 18:
        try:
            user_id = int(arg)
        except ValueError:
            user_id = 0
    else:
        user_id = 0

    return user_id


def translate_status(en_status: str) -> str:
    if en_status == 'dnd':
        return 'nie przeszkadzać'
    elif en_status == 'idle':
        return 'zaraz wracam'
    else:
        return en_status
