# -*- coding: utf-8 -*-


import numpy as np
import unittest
import yaml

from .. import ising


class TestIsing(unittest.TestCase):
    """ """

    params_file: str = "isypy/tests/params_ising_test.yml"

    @classmethod
    def setUp(self):
        pass

    def test_init(self):
        """ """

        with open(self.params_file, "r") as fin:
            yy_params = yaml.load(fin)
        ising_c = ising.Ising(yy_params)

        # Test that the given values are ok
        self.assertAlmostEqual(1.0, ising_c.beta)
        self.assertAlmostEqual(1.1, ising_c.h_field)
        self.assertAlmostEqual(-1.0, ising_c.Jparams["Jx"])
        self.assertAlmostEqual(-1.0, ising_c.Jparams["Jy"])
        self.assertAlmostEqual(0.0, ising_c.Jparams["Jz"])
        self.assertEqual(4, ising_c.spins.shape[0])
        self.assertEqual(4, ising_c.spins.shape[1])
        self.assertEqual(1, ising_c.spins.shape[2])
        self.assertAlmostEqual(4.0, ising_c.current["Magnetization"], places=3)

    def test_do_step(self):
        """ """

        with open(self.params_file, "r") as fin:
            yy_params = yaml.load(fin)
        ising_c = ising.Ising(yy_params)

        num_steps = int(1e6)
        for i in range(num_steps):
            ising_c.do_step()

        # self.assertAlmostEqual(0.9999, ising_c.current["Magnetization"], places=4)

    @unittest.skip("Not yet implemented.")
    def test_integration(self):
        pass


if __name__ == "__main__":
    unittest.main()
