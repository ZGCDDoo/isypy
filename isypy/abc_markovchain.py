import numpy as np  # type: ignore
from typing import Tuple
import abc


class ABCMarkovChain(abc.ABC):
    """ """

    def __init__(self) -> None:
        """ """
        return None

    @abc.abstractmethod
    def init_energy(self)->None:
        """ """
        return None

    @abc.abstractmethod
    def build_arr_perdiodic(self, NN: int):
        """Build numpy arrays that can be used with periodic boundary conditions"""
        return None

    @abc.abstractmethod
    def do_step(self)->None:
        """Perform one monte carlo update."""
        return None

    @abc.abstractmethod
    def measure(self)->None:
        """Perform one measurement for the current configuaration. """
        return None

    def save(self)->None:
        """Save the state."""
        return None
