# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

from . import monte_carlo
from . import ising
from . import tools


def run_isypy(jj_params) -> None:
    tools.println("Start Running isypy !")

    mc_machine = monte_carlo.MonteCarlo(jj_params, ising.Ising)
    mc_machine.run_simulation()
    return None
