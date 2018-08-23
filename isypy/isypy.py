# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

import time
import os
import sys
import mpi4py
import json


from . import monte_carlo


def run_isypy(temperature: float, Lx: int) -> None:
    print("Running isypy !")
    print("(Temperature, Lx) = ({0}, {1})".format(temperature, Lx))

    mc_machine = monte_carlo.MonteCarlo(0)
    mc_machine.thermalize()
    return None
