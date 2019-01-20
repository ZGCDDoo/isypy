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
    print(
        "Could not import mpi4py, running in serial mode. Consider running without mpirun. Stupido !"
    )


class MonteCarlo:

    """A Monte Carlo simulation runner
       """

    def __init__(self, yy_params, MarkovChainType) -> None:
        """

        Parameters
        ----------
        yy_params: yaml
            parameter file in yaml-object format
        MarkovChainType:
            The class that implements the interface given by abc_markovchain.
        """

        # init the seed
        if "mpi4py" in sys.modules:
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            yy_params["MonteCarlo"]["Seed"] = (
                yy_params["MonteCarlo"]["Seed"] + 1277 * rank
            )
            tools.println(f"Parallel mode, NWorkers = {comm.Get_size()}")

        self.MarkovChain = MarkovChainType(yy_params)
        self.yy_params = yy_params["MonteCarlo"]

        tools.println("Monte Carlo Class created !")

    def run_simulation(self) -> None:
        """ """
        tools.println("Start of Run Simulation")
        self.thermalize()
        self.measure()
        self.MarkovChain.save()
        tools.println("End of Run Simulation")

    def thermalize(self) -> None:
        """ """
        tools.println("Start Thermalization")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.yy_params["ThermalizationTime"])

        while timer.time_over():
            self.MarkovChain.do_step()

        tools.println("End Thermalization")

    def measure(self) -> None:
        """ """
        tools.println("Start Measurements")

        timer = timerpy.Timer()
        timer.start_countdown(60.0 * self.yy_params["MeasurementTime"])

        nsteps: int = 0
        upd_measure = self.yy_params["UpdatesMeasurement"]
        while not timer.time_over():
            for ii in range(upd_measure):
                self.MarkovChain.do_step()
                nsteps += 1

            self.MarkovChain.measure()

        tools.println("End Measurements")
