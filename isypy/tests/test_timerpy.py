# -*- coding: utf-8 -*-


import numpy as np
import unittest
import json

from .. import timerpy


class TestTimerPy(unittest.TestCase):
    """ """

    params_file: str = "isypy/tests/params_ising_test.json"

    def test_init(self):
        """ """
        timer = timerpy.Timer()


if __name__ == "__main__":
    unittest.main()
