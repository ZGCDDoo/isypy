# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""
import sys
import logging

try:
    from mpi4py import MPI
except ImportError:
    pass


def println(message: str) -> None:
    """Print with or without mpi. """

    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            print(message)
    else:
        print(message)

    sys.stdout.flush()


def log_info(message: str) -> None:
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            logging.info(message)


def log_warning(message: str) -> None:
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            logging.warning(message)


def log_debug(message: str) -> None:
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            logging.warning(message)


def log_error(message: str) -> None:
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            logging.error(message)


def log_critical(message: str) -> None:
    if "mpi4py" in sys.modules:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            logging.critical(message)
