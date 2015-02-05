Data File Format
=================

A data file can be training or evaluation data. Both files are ``.tar`` files.

The training data file ``train.tar`` has to contain a ``x.hdf5`` and a
``y.hdf5``. Both HDF5 files have to contain matrices. Let's call the matrix
in ``x.hdf5`` X and similarly the matrix in ``y.hdf5`` Y.
(The HDF files both contain exactly one object called ``x.hdf5`` or ``y.hdf5``)

X contains the features of all training examples and Y contains the labels.

Then $X \in \mathbb{R}^{n \times m}$ and $L \in \mathbb{n \times 1}$ where
$n$ is the number of training examples and $m$ is the number of features.
$L$ might be $\mathbb{N}$ or simply strings.

To look at HDF5 files, you can use `hdfview`.