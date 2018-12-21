# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""
from . import timerpy
from . import tools
import numpy as np
import sys

try:
    from mpi4py import MPI
except ImportError:
    print("Could not import mpi4py, running in serial mode. Consider running without mpirun. Stupido !")


class MonteCarlo(object):

    """A Monte Carlo simulation runner
       """

    def __init__(self, yy_params, MarkovChainType) ->None:
        """ Inits a Monte Carlo class.
        Args:
            yy_params: A yaml object containing the Monte Carlo configuration for the Simulation.

        Returns:
            None

        Raises:
            IOError:
        """
        self.MarkovChain = MarkovChainType(yy_params)
        self.yy_params = yy_params["MonteCarlo"]

        # init the random number of numpy
        if "mpi4py" in sys.modules:
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            np.random.seed(yy_params["MonteCarlo"]["Seed"] + 1277*rank)

        tools.println("Monte Carlo Class created !")
        return None

    def run_simulation(self)->None:
        """ """
        tools.println("Start of Run Simulation")
        self.thermalize()
        self.measure()
        self.MarkovChain.save()
        tools.println("End of Run Simulation")
        return None

    def thermalize(self) ->None:
        """ """
        tools.println("Start Thermalization")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.yy_params["ThermalizationTime"])

        while timer.time_over():
            self.MarkovChain.do_step()

        tools.println("End Thermalization")

        return None

    def measure(self)->None:
        """ """
        tools.println("Start Measurements")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.yy_params["MeasurementTime"])

        nsteps = 0
        upd_measure = self.yy_params["UpdatesMeasurement"]
        while timer.time_over():
            self.MarkovChain.do_step()
            nsteps += 1
            # print("nsteps = ", nsteps)
            if (nsteps % upd_measure) == 0:
                self.MarkovChain.measure()

        tools.println("End Measurements")

        return None
