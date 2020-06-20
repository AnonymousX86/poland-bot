# -*- coding: utf-8 -*-
from datetime import timezone


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
