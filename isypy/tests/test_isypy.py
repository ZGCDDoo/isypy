# -*- coding: utf-8 -*-


import numpy as np
import unittest
import yaml
import json

from .. import isypy


class TestIsypy(unittest.TestCase):
    """ """

    params_file: str = "isypy/tests/params_ising_test.yml"

    @classmethod
    def setUp(self):
        pass

    def test_run_isypy(self):
        """ """

        with open(self.params_file, "r") as fin:
            yy_params = yaml.load(fin)

        isypy.run_isypy(yy_params)

        results_good = {
            "Energy": -3.099,
            "Magnetization": 0.9999,
            "Specific_Heat": 0.0,
            "Magnetic_susceptibility": 0.0,
        }

        with open("ising.out") as fin:
            results = json.load(fin)

        for key in results_good.keys():
            self.assertAlmostEqual(results_good[key], results[key], places=2)


if __name__ == "__main__":
    unittest.main()
