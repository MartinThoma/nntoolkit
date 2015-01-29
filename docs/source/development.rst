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



Feedback
--------
General feedback can be sent to info@martin-thoma.de