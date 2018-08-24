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
        print("Start of Run Simulation")
        self.thermalize()
        self.measure()
        self.MarkovChain.save()
        print("End of Run Simulation")
        return None

    def thermalize(self) ->None:
        """ """
        print("Start Thermalization")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.jj_params["ThermalizationTime"])

        while timer.time_over():
            self.MarkovChain.do_step()

        print("End Thermalization")

        return None

    def measure(self)->None:
        """ """
        print("Start Measurements")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.jj_params["MeasurementTime"])

        nsteps = 0
        upd_measure = self.jj_params["UpdatesMeasurement"]
        while timer.time_over():
            self.MarkovChain.do_step()
            nsteps += 1
            # print("nsteps = ", nsteps)
            if (nsteps % upd_measure) == 0:
                self.MarkovChain.measure()

        print("End Measurements")

        return None
