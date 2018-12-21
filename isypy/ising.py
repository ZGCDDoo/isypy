# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

import numpy as np
import yaml
import json
import sys
from numpy.random import randint
from numpy.random import random as urng

try:
    from mpi4py import MPI
except ImportError:
    print("Ayaya, mpi4py not found. Ok ok, serial mode man !")


from . import abc_markovchain

# H = sum_{ij} J_{ij} S_i S_j + h Sum_{i}S_i

# J_ij as the hoppings in Hubbard model CTQMC cttg


class Ising(abc_markovchain.ABCMarkovChain):

    spin_up = -1
    spin_down = 1
    invalid = -9999
    invalidf = float(invalid)

    def __init__(self, yy_params)->None:
        """ """
        # 0.) Get the parameter values

        self.yy_params = yy_params["Model"]
        (Nx, Ny, Nz) = self.yy_params["LatticeSize"]

        self.beta = float(self.yy_params["Beta"])

        # 1.) Randomly initialize the spins
        self.spins = np.random.choice(
            [self.spin_down, self.spin_up], (Nx, Ny, Nz))

        # 2.) Calculate the energy and initialize the J matrix
        self.h_field = self.yy_params["HField"]
        self.Jparams = self.yy_params["JParameters"]
        assert len(self.Jparams) ==3 , "Miseria, more than 3 parameters for the J . Stupido !"

        self.upd = {"Proposed": 0, "Accepted": 0}
        self.obs = {"Energy": 0.0, "Magnetization": 0.0,
                    "Specific_Heat": 0.0, "Magnetic_susceptibility": 0.0, "NMeas": 0}

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
        (nxparr, nxmarr) = self.build_arr_perdiodic(shape_ss[0])
        (nyparr, nymarr) = self.build_arr_perdiodic(shape_ss[1])
        (nzparr, nzmarr) = self.build_arr_perdiodic(shape_ss[2])

        for ii in range(shape_ss[0]):
            for jj in range(shape_ss[1]):
                for kk in range(shape_ss[2]):
                    # periodic boundary conditions
                    if shape_ss[0] != 1:
                        energy += self.Jparams["Jx"] * self.spins[ii, jj, kk] * \
                            (self.spins[nxparr[ii], jj, kk] +
                             self.spins[nxmarr[ii], jj, kk])
                    if shape_ss[1] != 1:
                        energy += self.Jparams["Jy"] * self.spins[ii, jj, kk] * \
                            (self.spins[ii, nyparr[jj], kk] +
                             self.spins[ii, nymarr[jj], kk])
                    if shape_ss[1] != 1:
                        energy += self.Jparams["Jz"] * self.spins[ii, jj, kk] * \
                            (self.spins[ii, jj, nzparr[kk]] +
                             self.spins[ii, jj, nzmarr[kk]])

        energy /= 2.0
        energy -= self.h_field * self.magnetization()
        self.current["Energy"] = energy
        # print("Init energy = ", energy)
        # print(self.spins)
        return None

    def build_arr_perdiodic(self, NN: int):
        """ """
        nparr = np.arange(1, NN + 1)
        nparr[-1] = 0
        nmarr = np.arange(-1, NN - 1)
        nmarr[0] = NN - 1

        return (nparr, nmarr)

    def magnetization(self) ->float:
        """ """
        return float(np.sum(self.spins))

    def do_step(self)->None:
        """Only one  Monte Carlo Step implemented, which here, is a single spin flip
           In a next version do multiple spin flips
         """
        self.try_single_spin_flip()
        self.upd["Proposed"] += 1
        return None

    def try_single_spin_flip(self)->None:
        """ """

        (Nx, Ny, Nz) = self.spins.shape
        self.current["Spin_Flip"]["Indices"] = (
            randint(0, Nx), randint(0, Ny), randint(0, Nz))

        (nx, ny, nz) = self.current["Spin_Flip"]["Indices"]
        self.current["Spin_Flip"]["SpinValue"] = -self.spins[nx, ny, nz]

        # periodic boundary conditions
        (nxp1, nxm1) = (nx + 1 if nx != (Nx - 1) else 0,
                        nx - 1 if nx != 0 else (Nx - 1))

        (nyp1, nym1) = (ny + 1 if ny != (Ny - 1) else 0,
                        ny - 1 if ny != 0 else (Ny - 1))

        (nzp1, nzm1) = (nz + 1 if nz != (Nz - 1) else 0,
                        nz - 1 if nz != 0 else (Nz - 1))

        delta_energy = 0.0
        deltaspin = -2.0 * self.spins[nx, ny, nz]
        # Energy in x
        if Nx != 1:
            delta_energy += self.Jparams["Jx"] * deltaspin * \
                (self.spins[nxm1, ny, nz] + self.spins[nxp1, ny, nz])

        if Ny != 1:
            delta_energy += self.Jparams["Jy"] * deltaspin * \
                (self.spins[nx, nym1, nz] + self.spins[nx, nyp1, nz])
        if Nz != 1:
            delta_energy += self.Jparams["Jz"] * deltaspin * \
                (self.spins[nx, ny, nzm1] + self.spins[nx, ny, nzp1])

        delta_energy -= self.h_field * deltaspin

        self.current["DeltaEnergy"] = delta_energy
        self.current["Spin_Flip"]["Weight"] = np.exp(-self.beta * delta_energy)

        if urng() < self.current["Spin_Flip"]["Weight"]:
            self.accept_flip()

        return None

    def accept_flip(self)->None:
        """ """
        # print("Flip Accepted !")
        self.current["Energy"] += self.current["DeltaEnergy"]
        self.current["Magnetization"] = self.magnetization()
        self.spins[self.current["Spin_Flip"]["Indices"]
                   ] = self.current["Spin_Flip"]["SpinValue"]

        self.upd["Accepted"] += 1
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
                self.obs[key] /= float(self.obs["NMeas"] * self.spins.size)

        # gather the measurements dictionaries

        if "mpi4py" in sys.modules:
            comm = MPI.COMM_WORLD
            comm_size = comm.Get_size()
            rank = comm.Get_rank()
        
            obs_array = comm.gather(self.obs, root=0)
            
            if rank == 0:
                print("Parallel save !")
                obs_result = obs_array[0]
                for ii in range(1, comm_size):                
                    for key in obs_array[ii].keys():
                        obs_result[key] += obs_array[ii][key]/float(comm_size)

                file_out: str = "ising.out"
                with open(file_out, mode="a") as fout:
                    json.dump(obs_result, fout, indent=4)

                np.save("config.npy", self.spins)
                # print(self.upd)
        else:
            print("Serial Save !")
            np.save("config.npy", self.spins)
            file_out: str = "ising.out"
            with open(file_out, mode="a") as fout:
                json.dump(self.obs, fout, indent=4)
