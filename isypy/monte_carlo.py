# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import numpy as np
import scipy
from . import timerpy


class MonteCarlo(object):

    """A Monte Carlo simulation runner
       """

    def __init__(self, yy, MarkovChainType: int=0) ->None:
        """ Inits a Monte Carlo class.
        Args:
            yy: A yaml object containing the Monte Carlo configuration for the Simulation.

        Returns:
            None

        Raises:
            IOError:
        """
        self.yy = yy
        print("Monte Carlo Class created !")
        return None

    def thermalize(self) ->None:
        """ """

        timer = timerpy.Timer()
        timer.start_countdown(60)

        while timer.time_over():
            i = 0

        return None
