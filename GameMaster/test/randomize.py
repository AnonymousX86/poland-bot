# -*- coding: utf-8 -*-
import unittest

from GameMaster.utils.random import seed


class MyTestCase(unittest.TestCase):
    def test_seed(self):
        same = 0
        do_test = 100000
        max_value = 10
        max_percent = max_value ** -1 * 1.05
        for i in range(do_test):
            self.assertEqual(
                seed('a' * i, max_value),
                seed('a' * i, max_value),
                'Result is not the same with same arguments.'
            )
            if seed('a' * i) == seed('b' * i):
                same += 1
        self.assertLessEqual(
            round(same / do_test * 100) / 100,
            max_percent,
            f'Results are same in more than {max_percent * 10}%.'
        )


if __name__ == '__main__':
    unittest.main()
