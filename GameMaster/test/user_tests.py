# -*- coding: utf-8 -*-
from GameMaster.utils.users import check_mention


def test_mention():
    for m in [
        '<@!701742664931999744>',
        '701742664931999744',
        '<@!672448271792472095>',
        '672448271792472095'
    ]:
        c = check_mention(m)
        assert type(c) is int
        assert len(str(c)) == 18
