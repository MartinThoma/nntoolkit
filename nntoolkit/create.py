#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a neural network model file."""

import logging
import os
import tarfile
import random
import yaml
import h5py
import numpy
import theano

# nntoolkit modules
from nntoolkit import utils


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--type",
                        choices=["mlp"],
                        default="mlp",
                        dest="type",
                        help="which type of neural network do you want to "
                             "create?",
                        metavar="TYPE")
    parser.add_argument("-a", "--architecture",
                        dest="architecture",
                        help="""architecture of the network""",
                        default="160:500:369")
    parser.add_argument("-f", "--file",
                        dest="model_file",
                        help="write model file to MODEL_FILE",
                        metavar="MODEL_FILE")
    return parser


def xaviar10_weight_init(neurons_a, neurons_b):
    """Initialize the weights between a layer with ``neurons_a`` neurons
    and a layer with ``neurons_b`` neurons.

    Returns
    -------
    A neurons_a × neurons_b matrix.
    """
    fan_in = neurons_a
    fan_out = neurons_b - 2
    init_weight = 4.0*numpy.sqrt(6.0/(fan_in+fan_out))
    W = [numpy.random.uniform(low=-init_weight,
                              high=init_weight,
                              size=neurons_a)
         for _ in range(neurons_b)]
    return W


def is_valid_model_file(model_file_path):
    """Check if `model_file_path` is a valid model file."""
    if os.path.isfile(model_file_path):
        logging.error("'%s' already exists.", model_file_path)
        return False
    if not model_file_path.endswith(".tar"):
        logging.error("'%s' does not end with '.tar'.", model_file_path)
        return False
    return True


def create_hdf5s_for_layer(i, layer):
    """Create one HDF5 file for the weight matrix W and one for the bias vector
    b.
    """
    Wfile = h5py.File('W%i.hdf5' % i, 'w')
    Wfile.create_dataset(Wfile.id.name, data=layer['W'])
    Wfile.close()

    bfile = h5py.File('b%i.hdf5' % i, 'w')
    bfile.create_dataset(bfile.id.name, data=layer['b'])
    bfile.close()


def create_layers(neurons):
    """Create the layers of the neural network.

    Parameters
    ----------
    neurons : list of integers
        Indicates how many neurons are in which layer.

    Returns
    -------
    list of dictionaries :
        random variables for the weight matrix W and the bias vector b
    """
    layers_binary = []
    for neurons_b, neurons_a in zip(neurons, neurons[1:]):
        W = xaviar10_weight_init(neurons_a, neurons_b)
        b = [random.random() for _ in range(neurons_a)]
        # TODO: parse architecture string to allow arbitrary activation
        # functions
        layers_binary.append({'W': numpy.array(W, dtype=theano.config.floatX),
                              'b': numpy.array(b, dtype=theano.config.floatX),
                              'activation': 'Sigmoid'})
    layers_binary[-1]['activation'] = 'Softmax'
    return layers_binary


def main(nn_type, architecture, model_file):
    """Create a neural network file of ``nn_type`` with ``architecture``.
    Store it in ``model_file``.

    Parameters
    ----------
    nn_type : string
        e.g. 'mlp'
    model_file :
        A path which should end with .tar. The created model will be written
        there.
    """
    if not is_valid_model_file(model_file):
        return

    logging.info("Create %s with a %s architecture...", nn_type, architecture)

    filenames = ["model.yml"]  # "input_semantics.csv", "output_semantics.csv"

    if nn_type == 'mlp':
        # Create layers by looking at 'architecture'
        layers = []

        # TODO: the activation function could be here!
        neurons = list(map(int, architecture.split(':')))

        layers_binary = create_layers(neurons)

        utils.create_boilerplate_semantics_files(neurons)
        filenames.append("input_semantics.csv")
        filenames.append("output_semantics.csv")

    # Write layers
    for i, layer in enumerate(layers_binary):
        create_hdf5s_for_layer(i, layer)

        layers.append({'W': {'size': list(layer['W'].shape),
                             'filename': 'W%i.hdf5' % i},
                       'b': {'size': list(layer['b'].shape),
                             'filename': 'b%i.hdf5' % i},
                       'activation': layer['activation']})
        filenames.append('W%i.hdf5' % i)
        filenames.append('b%i.hdf5' % i)

        model = {'type': 'mlp', 'layers': layers}

    with open('model.yml', 'w') as f:
        yaml.dump(model, f, default_flow_style=False)

    # Create tar file
    with tarfile.open(model_file, "w:") as tar:
        for name in filenames:
            tar.add(name)

    # Remove temporary files which are now in tar file
    for filename in filenames:
        os.remove(filename)


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.type, args.architecture, args.model_file)
