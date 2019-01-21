.. _installation:

Installation
================================


Basic installation (no parallalization)
----------------------------------------

It is recommended to try the basic installation before trying the mpi version.
The installation steps are very simple:

.. code-block:: bash

    pip install isypy    




MPI installation
------------------
It is recommended to install pipenv first.

.. code-block:: bash

    pip install pipenv
    pipenv install isypy mpi4py
    pipenv shell
