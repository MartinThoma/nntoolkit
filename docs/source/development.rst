Develpment
==========

.. note:: You can skip this if you don't want to develop ``nntoolkit``. This
page explains how to contribute to ``nntoolkit``, the next pages explain how to
use ``nntoolkit``.


Project Structure
-----------------
The project is structured in several modules:

* *bin/nntoolkit*: The Python scripts which handles user interaction at the
  highest level. All subcommands have an own module, but at first the user
  input gets handled here.
* *nntoolkit/utils.py*: Utility functions that can be used in multiple scripts.
* *nntoolkit/create.py*: Create a neural network model file.
* *nntoolkit/train.py*: Train a neural network.
* *nntoolkit/evaluate.py*: Evaluate a neural network.
* *nntoolkit/test.py*: Test a neural network.

You can also print a dependency graph with the Python package ``snakefood``:

.. code:: bash

    $ sfood | sfood-graph  > dependencies.dot
    $ dot -Tpng dependencies.dot -s200 -o dependency-graph.png

which generates

.. image:: dependency-graph.png
    :height: 350px
    :align: center
    :alt: nntoolkit dependency graph

You might have to set


.. code:: text

    graph G { 
        graph [ dpi = 300 ]; 
        /* The rest of your graph here. */ 
    }


TODOs
-----
See issues on GitHub: github.com/MartinThoma/nntoolkit


Current State
-------------

* lines of code without tests: LOC (``make countc``)
* lines of test code: LOT (``make countt``)
* test coverage: cov (``make test``)
* pylint score: lint (``pylint nntoolkit``)
* cheesecake_index: (``make testall``)
* users: How many people do currently actively use / develop ``nntoolkit``?

::

    date,        LOC,  LOT, cov, lint, cheesecake_index, users, changes
    2015-01-29, 1061,   86, 56%, 9.21,          362/595,     2, minor
    2015-01-29, 1139,   86, 56%, 9.22,          408/595,     2, minor (and fixed pylint for cheesecake_index)


Pylint messages
---------------

Most (not all!) of those need to be fixed:

::

    $ pylint nntoolkit
    ************* Module nntoolkit.evaluate
    W: 13, 4: Redefining built-in 'open' (redefined-builtin)
    ************* Module nntoolkit.test
    W: 41, 4: Attempting to unpack a non-sequence defined at line 143 of nntoolkit.utils (unpacking-non-sequence)
    W: 41, 4: Attempting to unpack a non-sequence defined at line 147 of nntoolkit.utils (unpacking-non-sequence)
    W: 41, 4: Attempting to unpack a non-sequence defined at line 153 of nntoolkit.utils (unpacking-non-sequence)
    ************* Module nntoolkit.create
    W: 61, 0: TODO: the activation function could be here! (fixme)
    W: 75, 0: TODO: parse architecture string to allow arbitrary activation (fixme)
    R: 39, 0: Too many local variables (26/15) (too-many-locals)
    W: 72,21: Unused variable 'j' (unused-variable)
    ************* Module nntoolkit.train
    W:102, 0: TODO: Sigmoid - make dependant from activation function (fixme)
    W:130, 0: TODO: Eventually we miss training examples! (fixme)
    R: 61, 0: Too many arguments (6/5) (too-many-arguments)
    R: 61, 0: Too many local variables (30/15) (too-many-locals)
    E:103, 8: Assigning to function call which doesn't return (assignment-from-no-return)
    R:138, 0: Too many arguments (6/5) (too-many-arguments)
    W:149, 4: Attempting to unpack a non-sequence defined at line 143 of nntoolkit.utils (unpacking-non-sequence)
    W:149, 4: Attempting to unpack a non-sequence defined at line 147 of nntoolkit.utils (unpacking-non-sequence)
    W:149, 4: Attempting to unpack a non-sequence defined at line 153 of nntoolkit.utils (unpacking-non-sequence)
    ************* Module nntoolkit.utils
    W: 22, 4: Redefining built-in 'open' (redefined-builtin)
    W: 62, 9: Used * or ** magic (star-args)
    R: 69, 0: Too many local variables (17/15) (too-many-locals)
    W:122, 9: Used * or ** magic (star-args)
    R:170, 0: Too many local variables (17/15) (too-many-locals)
    R:  1, 0: Similar lines in 2 files
    ==nntoolkit.evaluate:15
    ==nntoolkit.train:13
    import nntoolkit.utils as utils


    def get_parser():
        """Return the parser object for this script."""
        from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
        parser = ArgumentParser(description=__doc__,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-m", "--model", (duplicate-code)
    R:  1, 0: Similar lines in 2 files
    ==nntoolkit.test:12
    ==nntoolkit.train:16
    def get_parser():
        """Return the parser object for this script."""
        from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
        parser = ArgumentParser(description=__doc__,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-m", "--model",
                            dest="model_file",
                            help="where is the model file (.tar) which should get " (duplicate-code)
    R:  1, 0: Similar lines in 2 files
    ==nntoolkit.evaluate:18
    ==nntoolkit.test:12
    def get_parser():
        """Return the parser object for this script."""
        from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
        parser = ArgumentParser(description=__doc__,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-m", "--model", (duplicate-code)


    Report
    ======
    372 statements analysed.

    Statistics by type
    ------------------

    +---------+-------+-----------+-----------+------------+---------+
    |type     |number |old number |difference |%documented |%badname |
    +=========+=======+===========+===========+============+=========+
    |module   |6      |6          |=          |100.00      |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |class    |0      |0          |=          |0           |0        |
    +---------+-------+-----------+-----------+------------+---------+
    |method   |0      |0          |=          |0           |0        |
    +---------+-------+-----------+-----------+------------+---------+
    |function |20     |20         |=          |100.00      |0.00     |
    +---------+-------+-----------+-----------+------------+---------+



    External dependencies
    ---------------------
    ::

        future 
          \-builtins (nntoolkit.utils,nntoolkit.evaluate)
        h5py (nntoolkit.create,nntoolkit.utils)
        nntoolkit 
          \-evaluate (nntoolkit.test)
        numpy (nntoolkit.create,nntoolkit.utils,nntoolkit.train,nntoolkit.test,nntoolkit.evaluate)
        pkg_resources (nntoolkit)
        theano (nntoolkit.create,nntoolkit.train)
          \-tensor (nntoolkit.train)
        yaml (nntoolkit.create,nntoolkit.utils)



    Raw metrics
    -----------

    +----------+-------+------+---------+-----------+
    |type      |number |%     |previous |difference |
    +==========+=======+======+=========+===========+
    |code      |471    |69.67 |471      |=          |
    +----------+-------+------+---------+-----------+
    |docstring |103    |15.24 |103      |=          |
    +----------+-------+------+---------+-----------+
    |comment   |40     |5.92  |40       |=          |
    +----------+-------+------+---------+-----------+
    |empty     |62     |9.17  |62       |=          |
    +----------+-------+------+---------+-----------+



    Duplication
    -----------

    +-------------------------+------+---------+-----------+
    |                         |now   |previous |difference |
    +=========================+======+=========+===========+
    |nb duplicated lines      |23    |23       |=          |
    +-------------------------+------+---------+-----------+
    |percent duplicated lines |3.112 |3.112    |=          |
    +-------------------------+------+---------+-----------+



    Messages by category
    --------------------

    +-----------+-------+---------+-----------+
    |type       |number |previous |difference |
    +===========+=======+=========+===========+
    |convention |0      |0        |=          |
    +-----------+-------+---------+-----------+
    |refactor   |9      |9        |=          |
    +-----------+-------+---------+-----------+
    |warning    |15     |15       |=          |
    +-----------+-------+---------+-----------+
    |error      |1      |1        |=          |
    +-----------+-------+---------+-----------+



    % errors / warnings by module
    -----------------------------

    +-------------------+-------+--------+---------+-----------+
    |module             |error  |warning |refactor |convention |
    +===================+=======+========+=========+===========+
    |nntoolkit.train    |100.00 |33.33   |33.33    |0.00       |
    +-------------------+-------+--------+---------+-----------+
    |nntoolkit.utils    |0.00   |20.00   |55.56    |0.00       |
    +-------------------+-------+--------+---------+-----------+
    |nntoolkit.create   |0.00   |20.00   |11.11    |0.00       |
    +-------------------+-------+--------+---------+-----------+
    |nntoolkit.test     |0.00   |20.00   |0.00     |0.00       |
    +-------------------+-------+--------+---------+-----------+
    |nntoolkit.evaluate |0.00   |6.67    |0.00     |0.00       |
    +-------------------+-------+--------+---------+-----------+



    Messages
    --------

    +--------------------------+------------+
    |message id                |occurrences |
    +==========================+============+
    |unpacking-non-sequence    |6           |
    +--------------------------+------------+
    |too-many-locals           |4           |
    +--------------------------+------------+
    |fixme                     |4           |
    +--------------------------+------------+
    |duplicate-code            |3           |
    +--------------------------+------------+
    |too-many-arguments        |2           |
    +--------------------------+------------+
    |star-args                 |2           |
    +--------------------------+------------+
    |redefined-builtin         |2           |
    +--------------------------+------------+
    |unused-variable           |1           |
    +--------------------------+------------+
    |assignment-from-no-return |1           |
    +--------------------------+------------+



    Global evaluation
    -----------------
    Your code has been rated at 9.22/10 (previous run: 9.22/10, +0.00)




Feedback
--------
General feedback can be sent to info@martin-thoma.de