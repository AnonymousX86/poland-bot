# -*- coding: utf-8 -*-
from random import seed as r_seed, randint


def seed(arg, max_value=10):
    r_seed(arg)
    return randint(1, max_value)
