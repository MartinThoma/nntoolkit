#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Evaluate a neural network."""

import logging
import os
import yaml
import tarfile
import h5py
import math
import numpy
import json
import csv
import tempfile
import shutil
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


def get_activation(activation_str):
    """Return a function that works on a numpy array."""
    sigmoid = numpy.vectorize(lambda x: 1./(1+math.exp(-x)))
    if activation_str == 'sigmoid':
        return sigmoid
    elif activation_str == 'softmax':
        return lambda x: numpy.divide(numpy.exp(x), numpy.sum(numpy.exp(x)))


def get_outputs(output_file):
    outputs = {}
    mode = 'rt'
    arguments = {'newline': '', 'encoding': 'utf8'}
    with open(output_file, mode, **arguments) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(spamreader):
            outputs[i] = row[0]
    return outputs


def get_model(modelfile):
    """Check if ``modelfile`` is valid."""
    if not os.path.isfile(modelfile):
        logging.error("File '%s' does not exist.", modelfile)
        return False
    if not tarfile.is_tarfile(modelfile):
        logging.error("'%s' is not a valid tar file.", modelfile)
        return False
    tar = tarfile.open(modelfile)
    filenames = tar.getnames()
    if 'model.yml' not in filenames:
        logging.error("'%s' does not have a model.yml.", modelfile)
        return False
    if 'input_semantics.csv' not in filenames:
        logging.error("'%s' does not have an input_semantics.csv.", modelfile)
        return False
    if 'output_semantics.csv' not in filenames:
        logging.error("'%s' does not have an output_semantics.csv.", modelfile)
        return False
    tarfolder = tempfile.mkdtemp()
    tar.extractall(path=tarfolder)
    tar.close()
    model_yml = yaml.load(open(os.path.join(tarfolder, 'model.yml')))
    if model_yml['type'] == 'mlp':
        layers = []
        for layer in model_yml['layers']:
            layertmp = {}

            f = h5py.File(os.path.join(tarfolder, layer['b']['filename']), 'r')
            layertmp['b'] = f[layer['b']['filename']].value

            f = h5py.File(os.path.join(tarfolder, layer['W']['filename']), 'r')
            layertmp['W'] = f[layer['W']['filename']].value

            layertmp['activation'] = get_activation(layer['activation'])

            layers.append(layertmp)
    model_yml['layers'] = layers
    inputs = {}

    # if sys.version_info.major < 3:
    #     mode = 'rb'
    #     arguments = {}
    # else:
    mode = 'rt'
    arguments = {'newline': '', 'encoding': 'utf8'}

    input_semantics_file = os.path.join(tarfolder, 'input_semantics.csv')
    with open(input_semantics_file, mode, **arguments) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(spamreader):
            inputs[i] = row[0]
    outputs = get_outputs(os.path.join(tarfolder, 'output_semantics.csv'))
    model_yml['inputs'] = inputs
    model_yml['outputs'] = outputs

    # Cleanup
    shutil.rmtree(tarfolder)
    return model_yml


def show_results(results, n=10, print_results=True):
    """Show the TOP n results of a classification."""
    # Print headline
    s = ""
    if len(results) == 0:
        s += "-- No results --"
    else:
        s += "{0:18s} {1:7s}\n".format("LaTeX Code", "Prob")
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
    if model['type'] == 'mlp':
        for layer in model['layers']:
            b, W, activation = layer['b'], layer['W'], layer['activation']
            x = numpy.dot(x, W)
            x = activation(x + b)
        x = x[0]
    return x


def get_results(model_output, output_semantics):
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

    :param features: List of floats
    :param print_results: Print results if True. Always return results.
    :returns: List of possible answers, reverse-sorted by probability.
    """
    model = get_model(modelfile)
    if not model:
        return []
    x = numpy.array([features])
    model_output = get_model_output(model, x)
    results = get_results(model_output, model['outputs'])

    if print_results:
        show_results(results, n=10)
    return results


def main_bash(modelfile, inputvec, print_results=True):
    """Evaluate the model described in ``modelfile`` with ``inputvec`` as
       input data.

    :param inputvec: List with one list as element. This list contains floats.
    :param print_results: Print results if True. Always return results.
    """
    features = json.load(open(inputvec))
    return main(modelfile, features, print_results)


if __name__ == '__main__':
    args = get_parser().parse_args()
    main_bash(args.modelfile, args.inputvec)
