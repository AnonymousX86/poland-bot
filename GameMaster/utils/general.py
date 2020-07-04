# -*- coding: utf-8 -*-
def sort_nested(list_):
    return sorted(list_, key=lambda x: x[1], reverse=True)
