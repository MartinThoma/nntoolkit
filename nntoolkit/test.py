#!/usr/bin/env python

"""Test a neural network."""

# Third party modules
import numpy

# First party modules
import nntoolkit.evaluate as evaluate
import nntoolkit.utils as utils


def main(model_file: str, test_data: str, verbose=True) -> float:
    """
    Evaluate a model

    Parameters
    ----------
    model_file : str
        Path to a model file
    test_data : str
        Path to a testdata.hdf5 file

    Returns
    -------
    Testing results
    """
    model = utils.get_model(model_file)
    data = utils.get_data(test_data)
    x_vec, y_vec = data
    correct = 0
    total = 0
    for x, y in zip(x_vec, y_vec):
        x = numpy.array([x])
        y_pred = evaluate.get_model_output(model, x)
        y_pred = numpy.argmax(y_pred)
        if y_pred == y[0]:
            correct += 1
        total += 1
        if verbose and total % 100 == 0:
            print("%i: %0.2f" % (total, float(correct) / total))
    print(
        "Correct: %i/%i = %0.2f of total correct"
        % (correct, total, float(correct) / total)
    )
    return float(correct) / total
