#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test a neural network."""

import numpy
import logging

# nntoolkit modules
import nntoolkit.utils as utils
import nntoolkit.evaluate as evaluate


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model_file",
                        help="where is the model file (.tar) which should get "
                             "tested?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    parser.add_argument("-i", "--input",
                        dest="test_data",
                        help="""a file which contains testing data (.tar)""",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    return parser


def main(model_file, test_data, verbose=True):
    """ Evaluate a model

    Parameters
    ----------
    model_file : string
        Path to a model file
    test_data : string
        Path to a testdata.tar file

    Returns
    -------
    Testing results
    """
    model = utils.get_model(model_file)
    data = utils.get_data(test_data)
    if data is None:
        logging.error("Data could not be loaded. Stop testing.")
        return
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
            print("%i: %0.2f" % (total, float(correct)/total))
    print("Correct: %i/%i = %0.2f of total correct" %
          (correct, total, float(correct)/total))
    return float(correct)/total

if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.model_file, args.test_data)
