# -*- coding: utf-8 -*-
def nth_place(place: int) -> str:
    if place == 1:
        return ':first_place:'
    elif place == 2:
        return ':second_place:'
    elif place == 3:
        return ':third_place:'
    else:
        return f'{place})'
