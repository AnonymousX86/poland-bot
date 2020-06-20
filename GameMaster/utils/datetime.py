# -*- coding: utf-8 -*-
from datetime import timezone, datetime as d


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def delta_time(start_time):
    return int(round((d.timestamp(d.now()) - start_time) * 1000, 0))
