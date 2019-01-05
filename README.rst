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
2. $ cd isypy/isypy/tests && python -m isypy params_ising.yml

To run your own simulation simply copy the file params_ising.yml from step 2
and change the self-explanatory parameters to your likeing.


Running with openmpi
************************

1. install mpi4py: pip install mpi4py
2. run the test with mpirun, with say 4 processes: mpirun -np 4 python -m isypy params_ising.yml