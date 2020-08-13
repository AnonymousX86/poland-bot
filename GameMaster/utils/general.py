# -*- coding: utf-8 -*-
from typing import List


def sort_nested(list_: list, reversed_: bool = False) -> List[List]:
    return sorted(list_, key=lambda x: x[1], reverse=reversed_)
