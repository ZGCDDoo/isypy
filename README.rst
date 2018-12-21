.. image:: https://travis-ci.org/ZGCDDoo/Isypy.svg?branch=master
    :target: https://travis-ci.org/ZGCDDoo/Isypy
   
.. image:: https://codecov.io/gh/ZGCDDoo/isypy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ZGCDDoo/isypy

Isypy
=======

Simple Monte Carlo Solver for the Ising model in 1, 2 or three dimensions. 


Requirements 
-------------
* Tested on python3.6.2 (will not work on python2)

Installation
-------------
1. $ cd isypy # (go to directory with the setup.py file)
2. $ pip install -e .

Running tests and examples
---------------------------
1. $ cd isypy && python -m unittest discover
2. $ cd isypy/isypy/tests && python -m isypy params_ising.json