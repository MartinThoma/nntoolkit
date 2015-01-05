Model File Format
=================

A model describes a neural network. It is a tar file which contains some other
files:

* ``model.yml``: A YAML file which describes the neural network
* ``input_semantics.csv``: A file which has exactly one line for every input
  neuron. It can be used to describe semantically what the inputs mean. If no
  semantics are wished, the line could contain ``input [LINE NR]``.
* ``output_semantics.csv``: Similar to input semantics.

model.yml
~~~~~~~~~

One example for a ``model.yml`` is

.. code-block:: text

    type: mlp
    layers:
    - W:
        filename: W0.hdf5
        size:
        - 167
        - 500
      activation: sigmoid
      b:
        filename: b0.hdf5
        size:
        - 500
    - W:
        filename: W1.hdf5
        size:
        - 500
        - 500
      activation: sigmoid
      b:
        filename: b1.hdf5
        size:
        - 500
    - W:
        filename: W2.hdf5
        size:
        - 500
        - 369
      activation: softmax
      b:
        filename: b2.hdf5
        size:
        - 369

The content might be different for other model types. Each layer has a weight
matrix ``W`` and a bias vector ``b``. They are stored in HDF5 files.