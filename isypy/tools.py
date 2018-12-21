# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""
import sys

try:
    from mpi4py import MPI
except ImportError:
    pass


def println(message:str)->None:
    """Print with or without mpi. """
    
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            print(message)
    else:
        print(message)
    
    return None

 