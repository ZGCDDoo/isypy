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
# H = sum_{ij} J_{ij} S_i S_j + h Sum_{i}S_i

# J_ij as the hoppings in Hubbard model CTQMC cttg


class Ising(object):

    spin_up = -1
    spin_down = 1

    def __init__(self, jj_params)->None:
        """ """
        # 0.) Get the parameter values
        (Nx, Ny, Nz) = jj_params["LatticeSize"]
        self.beta = jj_params["Beta"]
        np.random.seed(jj["Seed"])

        # 1.) Randomly initialize the spins
        self.spins = np.random.choice(
            [self.spin_down, self.spin_up], (Nx, Ny, Nz))

        # 2.) Calculate the energy and initialize the J matrix
        self.Jparams = jj_params["JParameters"]
        self.obs = {"Energy": 0.0, "Magnetization": 0.0}
        self.init_energy()

        return None

    def init_energy(self)->None:
        """ """
        shape_ss = self.spins.shape
        assert len(shape_ss) == 3
        energy: float = 0.0
        for nx in shape_ss[0]:
            for ny in shape_ss[1]:
                for nz in shape_ss[2]:
                    nxp1 = nx + 1 if nx != (shape_ss[0] - 1) else 0
                    nyp1 = ny + 1 if ny != (shape_ss[1] - 1) else 0
                    nzp1 = nz + 1 if nz != (shape_ss[2] - 1) else 0

                    energy += self.Jparams["Jx"] * self.spins[nx,
                                                              ny, nz] * self.spins[nxp1, ny, nz]
                        +
                        self.Jparams["Jy"] * self.spins[nx, ny, nz] * self.spins[nx, nyp1, nz]+
                        self.Jparams["Jz"] * self.spins[nx, ny,
                                                        nz] * self.spins[nx, ny, nzp1]

        energy += self.h_field * magnetization()
        self.obs["Energy"] = energy
        return None

    def update_energy(self, )->float:
        """ """

        return 0.0

    def magnetization(self) ->float:
        """ """
        return (np.sum(self.spins))

    def weight_single_spin_flip(self)->float:

        return np.exp(1.0) / np.exp(1.0)
