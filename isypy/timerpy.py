# -*- coding: utf-8 -*-
"""
@author: Charles-David Hebert
"""

import time


class Timer(object):

    def __init__(self)->None:
        """ """
        self.start = time.perf_counter()
        self.countdown = 0.0
        self.reset()
        return None

    def reset(self)->None:
        self.start = time.perf_counter() - self.start
        return None

    def start_countdown(self, countdown: float) ->None:
        """ """
        self.reset()
        self.countdown = countdown
        return None

    def time_over(self)->bool:
        # print("time.perf_counter()  = {0}, self.start = {1}, self.countdown = {2}".format(
        #   time.perf_counter(), self.start, self.countdown))
        return bool((time.perf_counter() - self.start) < self.countdown)
