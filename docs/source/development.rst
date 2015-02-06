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
    2015-01-31, 1333,  181, 56%, 9.26,          408/595,     2, minor (removed star-argument)
    2015-02-06, 1235,  164, 58%, 9.17,          408/595,     2, minor


Pylint messages
---------------

Most (not all!) of the following pylint issues need to be fixed. What does
not need any attention is

* "Redefining built-in 'open'" when it is ``from future.builtins import open``

::

    $ pylint nntoolkit
    ************* Module nntoolkit.activation_functions
    W: 12,20: Unused argument 'config_key' (unused-argument)
    ************* Module nntoolkit.evaluate
    W: 13, 4: Redefining built-in 'open' (redefined-builtin)
    ************* Module nntoolkit.test
    W: 46, 4: Attempting to unpack a non-sequence defined at line 142 of nntoolkit.utils (unpacking-non-sequence)
    W: 46, 4: Attempting to unpack a non-sequence defined at line 146 of nntoolkit.utils (unpacking-non-sequence)
    W: 46, 4: Attempting to unpack a non-sequence defined at line 152 of nntoolkit.utils (unpacking-non-sequence)
    ************* Module nntoolkit.create
    W: 87, 0: TODO: parse architecture string to allow arbitrary activation (fixme)
    W:121, 0: TODO: the activation function could be here! (fixme)
    C: 39, 0: Missing function docstring (missing-docstring)
    W: 46,13: Unused variable 'j' (unused-variable)
    C: 50, 0: Missing function docstring (missing-docstring)
    C: 59, 0: Missing function docstring (missing-docstring)
    C: 71, 0: Missing function docstring (missing-docstring)
    C: 81, 0: Missing function docstring (missing-docstring)
    W: 86,33: Unused variable 'i' (unused-variable)
    W:124,23: Unused variable 'layer_counter' (unused-variable)
    ************* Module nntoolkit.train
    W:102, 0: TODO: Sigmoid - make dependant from activation function (fixme)
    W:131, 0: TODO: Eventually we miss training examples! (fixme)
    R: 61, 0: Too many arguments (6/5) (too-many-arguments)
    R: 61, 0: Too many local variables (30/15) (too-many-locals)
    E:103, 8: Assigning to function call which doesn't return (assignment-from-no-return)
    R:139, 0: Too many arguments (6/5) (too-many-arguments)
    W:150, 4: Attempting to unpack a non-sequence defined at line 142 of nntoolkit.utils (unpacking-non-sequence)
    W:150, 4: Attempting to unpack a non-sequence defined at line 146 of nntoolkit.utils (unpacking-non-sequence)
    W:150, 4: Attempting to unpack a non-sequence defined at line 152 of nntoolkit.utils (unpacking-non-sequence)
    ************* Module nntoolkit.utils
    W: 23, 4: Redefining built-in 'open' (redefined-builtin)
    C: 60, 0: Missing function docstring (missing-docstring)
    W:121, 9: Used * or ** magic (star-args)
    C:169, 0: Missing function docstring (missing-docstring)
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
    ==nntoolkit.test:13
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
    ==nntoolkit.test:13
    def get_parser():
        """Return the parser object for this script."""
        from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
        parser = ArgumentParser(description=__doc__,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-m", "--model", (duplicate-code)


    Report
    ======
    422 statements analysed.

    Statistics by type
    ------------------

    +---------+-------+-----------+-----------+------------+---------+
    |type     |number |old number |difference |%documented |%badname |
    +=========+=======+===========+===========+============+=========+
    |module   |7      |6          |+1.00      |100.00      |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |class    |2      |0          |+2.00      |100.00      |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |method   |6      |0          |+6.00      |100.00      |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |function |28     |20         |+8.00      |75.00       |0.00     |
    +---------+-------+-----------+-----------+------------+---------+



    External dependencies
    ---------------------
    ::

        future 
          \-builtins (nntoolkit.utils,nntoolkit.evaluate)
        h5py (nntoolkit.create,nntoolkit.utils)
        nntoolkit 
          \-activation_functions (nntoolkit.utils)
          \-evaluate (nntoolkit.test)
        numpy (nntoolkit.activation_functions,nntoolkit.create,nntoolkit.train,nntoolkit.test,nntoolkit.evaluate)
        pkg_resources (nntoolkit)
        theano (nntoolkit.create,nntoolkit.train)
          \-tensor (nntoolkit.train)
        yaml (nntoolkit.create,nntoolkit.utils)



    Raw metrics
    -----------

    +----------+-------+------+---------+-----------+
    |type      |number |%     |previous |difference |
    +==========+=======+======+=========+===========+
    |code      |524    |67.70 |474      |+50.00     |
    +----------+-------+------+---------+-----------+
    |docstring |117    |15.12 |103      |+14.00     |
    +----------+-------+------+---------+-----------+
    |comment   |57     |7.36  |40       |+17.00     |
    +----------+-------+------+---------+-----------+
    |empty     |76     |9.82  |63       |+13.00     |
    +----------+-------+------+---------+-----------+



    Duplication
    -----------

    +-------------------------+------+---------+-----------+
    |                         |now   |previous |difference |
    +=========================+======+=========+===========+
    |nb duplicated lines      |23    |23       |=          |
    +-------------------------+------+---------+-----------+
    |percent duplicated lines |2.687 |3.096    |-0.41      |
    +-------------------------+------+---------+-----------+



    Messages by category
    --------------------

    +-----------+-------+---------+-----------+
    |type       |number |previous |difference |
    +===========+=======+=========+===========+
    |convention |7      |0        |+7.00      |
    +-----------+-------+---------+-----------+
    |refactor   |6      |9        |-3.00      |
    +-----------+-------+---------+-----------+
    |warning    |17     |14       |+3.00      |
    +-----------+-------+---------+-----------+
    |error      |1      |1        |=          |
    +-----------+-------+---------+-----------+



    % errors / warnings by module
    -----------------------------

    +-------------------------------+-------+--------+---------+-----------+
    |module                         |error  |warning |refactor |convention |
    +===============================+=======+========+=========+===========+
    |nntoolkit.train                |100.00 |29.41   |50.00    |0.00       |
    +-------------------------------+-------+--------+---------+-----------+
    |nntoolkit.create               |0.00   |29.41   |0.00     |71.43      |
    +-------------------------------+-------+--------+---------+-----------+
    |nntoolkit.test                 |0.00   |17.65   |0.00     |0.00       |
    +-------------------------------+-------+--------+---------+-----------+
    |nntoolkit.utils                |0.00   |11.76   |50.00    |28.57      |
    +-------------------------------+-------+--------+---------+-----------+
    |nntoolkit.evaluate             |0.00   |5.88    |0.00     |0.00       |
    +-------------------------------+-------+--------+---------+-----------+
    |nntoolkit.activation_functions |0.00   |5.88    |0.00     |0.00       |
    +-------------------------------+-------+--------+---------+-----------+



    Messages
    --------

    +--------------------------+------------+
    |message id                |occurrences |
    +==========================+============+
    |missing-docstring         |7           |
    +--------------------------+------------+
    |unpacking-non-sequence    |6           |
    +--------------------------+------------+
    |fixme                     |4           |
    +--------------------------+------------+
    |unused-variable           |3           |
    +--------------------------+------------+
    |duplicate-code            |3           |
    +--------------------------+------------+
    |too-many-arguments        |2           |
    +--------------------------+------------+
    |redefined-builtin         |2           |
    +--------------------------+------------+
    |unused-argument           |1           |
    +--------------------------+------------+
    |too-many-locals           |1           |
    +--------------------------+------------+
    |star-args                 |1           |
    +--------------------------+------------+
    |assignment-from-no-return |1           |
    +--------------------------+------------+



    Global evaluation
    -----------------
    Your code has been rated at 9.17/10 (previous run: 9.26/10, -0.08)





Feedback
--------
General feedback can be sent to info@martin-thoma.de