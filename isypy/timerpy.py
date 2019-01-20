# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

import time


class Timer:
    """A simple timer class that implements a countdown in seconds.


    Attributes
    ----------
    start : time
        The time at which the countdown starts.
    countdown : time
        The amount of time to count_down.

    """

    def __init__(self) -> None:

        self.start = time.perf_counter()
        self.countdown = 0.0
        self.reset()

    def reset(self) -> None:
        self.start = time.perf_counter() - self.start

    def start_countdown(self, countdown: float) -> None:

        self.reset()
        self.countdown = countdown

    def time_over(self) -> bool:
        return time.perf_counter() - self.start > self.countdown
