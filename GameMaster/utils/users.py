# -*- coding: utf-8 -*-
warn_roles_ids = {
    1: 713401249797505135,
    2: 713401427929858069,
    3: 713401508292591777
}


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
