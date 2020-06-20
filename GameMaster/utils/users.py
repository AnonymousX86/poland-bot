# -*- coding: utf-8 -*-
warn_roles_ids = {
    1: 713401249797505135,
    2: 713401427929858069,
    3: 713401508292591777
}


def check_mention(user_id: str):
    if len(user_id) == 21:
        user_id = user_id[2:-1]
    elif len(user_id) == 22:
        user_id = user_id[3:-1]
    if len(user_id) == 18:
        try:
            user_id = int(user_id)
        except ValueError:
            pass
    return user_id
