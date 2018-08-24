# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

import time
import os
import sys
import mpi4py
import json


import numpy as np
from numpy.random import randint
from numpy.random import random as urng

# H = sum_{ij} J_{ij} S_i S_j + h Sum_{i}S_i

# J_ij as the hoppings in Hubbard model CTQMC cttg


class Ising(object):

    spin_up = -1
    spin_down = 1
    invalid = -9999
    invalidf = float(invalid)

    def __init__(self, jj_params)->None:
        """ """
        # 0.) Get the parameter values
        (Nx, Ny, Nz) = jj_params["LatticeSize"]
        self.beta = float(jj_params["Beta"])
        np.random.seed(jj_params["Seed"])

        # 1.) Randomly initialize the spins
        self.spins = np.random.choice(
            [self.spin_down, self.spin_up], (Nx, Ny, Nz))

        # 2.) Calculate the energy and initialize the J matrix
        self.h_field = jj_params["HField"]
        self.Jparams = jj_params["JParameters"]
        self.obs = {"Energy": 0.0, "Magnetization": 0.0,
                    "Specific_Heat": 0.0, "Magnetic_susceptibility": 0.0, "NMeas": 0, "AcceptedFlips": 0}

        # When we try a spin flip, it is not immediatly accepted,thus, cache the values
        # and accept only in the method accept_move
        # DeltaEnergy = E' - E, with E' the energy of the system with the spin flipped
        self.current = {"Spin_Flip": {"Indices": (self.invalid, self.invalid, self.invalid), "DeltaEnergy": self.invalidf, "SpinValue": self.invalid, "Weight": self.invalid},
                        "Energy": self.invalidf, "Magnetization": self.magnetization()}

        self.init_energy()
        return None

    def init_energy(self)->None:
        """ """
        shape_ss = self.spins.shape
        assert len(shape_ss) == 3
        energy: float = 0.0

        for nx in range(shape_ss[0]):
            for ny in range(shape_ss[1]):
                for nz in range(shape_ss[2]):
                    # periodic boundary conditions
                    nxp1 = nx + 1 if nx != (shape_ss[0] - 1) else 0
                    nyp1 = ny + 1 if ny != (shape_ss[1] - 1) else 0
                    nzp1 = nz + 1 if nz != (shape_ss[2] - 1) else 0

                    if shape_ss[0] != 1:
                        energy += self.Jparams["Jx"] * self.spins[nx,
                                                                  ny, nz] * self.spins[nxp1, ny, nz]
                    if shape_ss[1] != 1:
                        energy += self.Jparams["Jy"] * self.spins[nx,
                                                                  ny, nz] * self.spins[nx, nyp1, nz]
                    if shape_ss[1] != 1:
                        energy += self.Jparams["Jz"] * self.spins[nx,
                                                                  ny, nz] * self.spins[nx, ny, nzp1]

        energy -= self.h_field * self.magnetization()
        self.current["Energy"] = energy
        return None

    def magnetization(self) ->float:
        """ """
        return float(np.sum(self.spins))

    def do_step(self)->None:
        """Only one  Monte Carlo Step implemented, which here, is a single spin flip
           In a next version do multiple spin flips
         """
        self.try_single_spin_flip()
        return None

    def try_single_spin_flip(self)->None:
        """ """

        (Nx, Ny, Nz) = self.spins.shape
        self.current["Spin_Flip"]["Indices"] = (
            randint(0, Nx), randint(0, Ny), randint(0, Nz))

        (nx, ny, nz) = self.current["Spin_Flip"]["Indices"]
        self.current["Spin_Flip"]["SpinValue"] = -self.spins[nx, ny, nz]

        delta_energy = -self.current["Energy"]

        # periodic boundary conditions
        nxp1 = nx + 1 if nx != (Nx - 1) else 0
        nyp1 = ny + 1 if ny != (Ny - 1) else 0
        nzp1 = nz + 1 if nz != (Nz - 1) else 0
        nxm1 = nx - 1 if nx != 0 else (Nx - 1)
        nym1 = ny - 1 if ny != 0 else (Ny - 1)
        nzm1 = nz - 1 if nz != 0 else (Nz - 1)

        # Energy in x
        if Nx != 1:
            delta_energy += self.Jparams["Jx"] * self.spins[nx, ny, nz] * \
                (self.spins[nxm1, ny, nz] + self.spins[nxp1, ny, nz])

        if Ny != 1:
            delta_energy += self.Jparams["Jy"] * self.spins[nx, ny, nz] * \
                (self.spins[nx, nym1, nz] + self.spins[nx, nyp1, nz])
        if Nz != 1:
            delta_energy += self.Jparams["Jz"] * self.spins[nx, ny, nz] * \
                (self.spins[nx, ny, nzm1] + self.spins[nx, ny, nzp1])

        delta_energy -= self.h_field * self.current["Spin_Flip"]["SpinValue"]

        self.current["DeltaEnergy"] = delta_energy
        self.current["Spin_Flip"]["Weight"] = np.exp(-self.beta * delta_energy)

        if urng() < self.current["Spin_Flip"]["Weight"]:
            self.accept_flip()

        return None

    def accept_flip(self)->None:
        """ """
        self.current["Energy"] += self.current["DeltaEnergy"]
        self.current["Magnetization"] = self.magnetization()
        self.spins[self.current["Spin_Flip"]["Indices"]
                   ] = self.current["Spin_Flip"]["SpinValue"]

        self.obs["AcceptedFlips"] += 1
        return None

    def measure(self)->None:
        """ """
        # print("Start Ising Measuring !")

        self.current["Magnetization"] = self.magnetization()
        self.obs["Magnetization"] += self.current["Magnetization"]
        self.obs["Energy"] += self.current["Energy"]
        self.obs["NMeas"] += 1

        # print("End Ising Measuring !")
        return None

    def save(self)->None:
        """Save the state"""
        for key in self.obs.keys():
            if key != "NMeas":
                self.obs[key] /= self.obs["NMeas"]

        file_out: str = "ising.out"
        with open(file_out, mode="a") as fout:
            json.dump(self.obs, fout, indent=4)

        np.savetxt("config.dat", self.spins)
