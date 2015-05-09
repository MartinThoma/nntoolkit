#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Evaluate a neural network."""

import numpy
import json
import sys

PY3 = sys.version > '3'

if not PY3:
    from future.builtins import open

# nntoolkit modules
import nntoolkit.utils as utils


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="modelfile",
                        help="where is the model file (.tar)?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    parser.add_argument("-i", "--input",
                        dest="inputvec",
                        help="""a file which contains an input vector
                               [[0.12, 0.312, 1.21 ...]]""",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    return parser


def show_results(results, n=10, print_results=True):
    """Show the top-n results of a classification."""
    # Print headline
    s = ""
    if len(results) == 0:
        s += "-- No results --"
    else:
        s += "{0:18s} {1:7s}\n".format("Class", "Prob")
        s += "#"*50 + "\n"
        for entry in results:
            if n == 0:
                break
            else:
                n -= 1
            s += "{0:18s} {1:>7.4f}%\n".format(entry['semantics'],
                                               entry['probability']*100)
        s += "#"*50
    if print_results:
        print(s)
    return s


def get_model_output(model, x):
    """
    Parameters
    ----------
    model : dict
        represents a model
    x : An input vector

    Returns
    -------
    The output vector of the model
    """
    if model['type'] == 'mlp':
        for layer in model['layers']:
            b, W, activation = layer['b'], layer['W'], layer['activation']
            x = numpy.dot(x, W)
            x = activation(x + b)
        x = x[0]
    return x


def get_results(model_output, output_semantics):
    """
    Parameters
    ----------
    model_output : list
        A list of probabilities
    output_semantics : list
        A list of semantics

    Returns
    -------
    A list of dictionaries which have probability and semantics as keys.
    """
    results = []
    for symbolnr, prob in enumerate(model_output):
        results.append({'symbolnr': symbolnr,
                        'probability': prob,
                        'semantics': output_semantics[symbolnr]})
    results = sorted(results, key=lambda x: x['probability'], reverse=True)
    return results


def main(modelfile, features, print_results=True):
    """Evaluate the model described in ``modelfile`` with ``inputvec`` as
    input data.

    Parameters
    ----------
    features : list of floats
    print_results : bool
        Print results if True. Always return results.

    Returns
    -------
    List of possible answers, reverse-sorted by probability.
    """
    model = utils.get_model(modelfile)
    if not model:
        return []
    x = numpy.array([features])
    model_output = get_model_output(model, x)
    results = get_results(model_output, model['outputs'])

    if print_results:
        show_results(results, n=10)
    return results


def main_bash(modelfile, inputvec_file, print_results=True):
    """Evaluate the model described in ``modelfile`` with ``inputvec_file`` as
       input data.

    Parameters
    ----------
    inputvec_file :
        File with json content. The content is a list with one list as element.
        This list contains floats.
    print_results : bool
        Print results if True.

    Returns
    -------
    results
    """
    features = json.load(open(inputvec_file))
    return main(modelfile, features, print_results)


if __name__ == '__main__':
    args = get_parser().parse_args()
    main_bash(args.modelfile, args.inputvec)
