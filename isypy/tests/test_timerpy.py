# -*- coding: utf-8 -*-


import unittest
from .. import timerpy


class TestTimerPy(unittest.TestCase):
    """ """

    params_file: str = "isypy/tests/params_ising_test.json"

    def test_init(self):
        """ """
        _ = timerpy.Timer()


if __name__ == "__main__":
    unittest.main()
