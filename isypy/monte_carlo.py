# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""
from . import timerpy


class MonteCarlo(object):

    """A Monte Carlo simulation runner
       """

    def __init__(self, jj_params, MarkovChainType) ->None:
        """ Inits a Monte Carlo class.
        Args:
            jj_params: A json object containing the Monte Carlo configuration for the Simulation.

        Returns:
            None

        Raises:
            IOError:
        """
        self.jj_params = jj_params
        self.MarkovChain = MarkovChainType(jj_params)

        print("Monte Carlo Class created !")
        return None

    def run_simulation(self)->None:
        """ """
        return None

    def thermalize(self) ->None:
        """ """

        timer = timerpy.Timer()
        timer.start_countdown(60)

        while timer.time_over():
            self.MarkovChain.do_step()

        return None

    def measure()->None:

        return None
