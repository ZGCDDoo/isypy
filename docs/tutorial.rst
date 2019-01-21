.. _tutorial:

Tutorial
==========

Once **isypy** is installed, copy the following yaml code in a file called to your liking, why not **params.yml**.

.. code-block:: yaml

  ---

  MonteCarlo:
    ThermalizationTime: 0.15
    MeasurementTime: 1.0
    UpdatesMeasurement: 100
    Seed: 1204

  Model:
    LatticeSize: [4, 4, 1]
    Beta: 1.0
    HField: 1.1
    JParameters:
      Jx: -1.0
      Jy: -1.0
      Jz: 0.0

Please ensure that the idention is the same as above. In doubt, please lint your file with the tool *yamllint*.
The simulation can be run by using the following command:

.. code-block:: bash
    
    python -m isypy params.yml

Or if you have installed with *mi4py*, and you want to use 4 processors:

.. code-block:: bash
    
    mpirun -np 4 python -m isypy params.yml





