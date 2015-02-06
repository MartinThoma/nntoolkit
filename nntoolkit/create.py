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
    fan_in = neurons_a
    fan_out = neurons_b - 2
    init_weight = 4.0*numpy.sqrt(6.0/(fan_in+fan_out))
    W = [numpy.random.uniform(low=-init_weight,
                              high=init_weight,
                              size=neurons_a)
         for j in range(neurons_b)]
    return W


def file_validate(model_file):
    if os.path.isfile(model_file):
        logging.error("'%s' already exists.", model_file)
        raise IOError
    if not model_file.endswith(".tar"):
        logging.error("'%s' does not end with '.tar'.", model_file)
        raise IOError


def create_semantics_io_files(neurons):
    # Create and add input_semantics.csv
    with open("input_semantics.csv", 'w') as f:
        for i in range(neurons[0]):
            f.write("input neuron %i\n" % i)

    # Create and add output_semantics.csv
    with open("output_semantics.csv", 'w') as f:
        for i in range(neurons[-1]):
            f.write("output neuron %i\n" % i)


def hdf5_file_write(i, layer):
    Wfile = h5py.File('W%i.hdf5' % i, 'w')
    Wfile.create_dataset(Wfile.id.name, data=layer['W'])
    Wfile.close()

    bfile = h5py.File('b%i.hdf5' % i, 'w')
    bfile.create_dataset(bfile.id.name, data=layer['b'])
    bfile.close()


def create_layers(neurons):
    layer_counter = 0
    layers_binary = []
    for neurons_b, neurons_a in zip(neurons, neurons[1:]):
        W = xaviar10_weight_init(neurons_a, neurons_b)
        b = [random.random() for i in range(neurons_a)]
        # TODO: parse architecture string to allow arbitrary activation
        # functions
        if layer_counter + 2 == len(neurons):
            layer_activation = 'softmax'
        else:
            layer_activation = 'sigmoid'

        layers_binary.append({'W': numpy.array(W, dtype=theano.config.floatX),
                              'b': numpy.array(b, dtype=theano.config.floatX),
                              'activation': layer_activation})
        layer_counter += 1
    return layers_binary, layer_counter


def main(nn_type, architecture, model_file):
    """Create a neural network file of ``nn_type`` with ``architecture``.
       Store it in ``model_file``.
       :param nn_type: A string, e.g. 'mlp'
       :param model_file: A path which should end with .tar. The created model
       will be written there.
    """
    try:
        file_validate(model_file)
    except IOError:
        return

    logging.info("Create %s with a %s architecture...", nn_type, architecture)

    filenames = ["model.yml"]  # "input_semantics.csv", "output_semantics.csv"

    if nn_type == 'mlp':
        # Create layers by looking at 'architecture'
        layers = []

        # TODO: the activation function could be here!
        neurons = list(map(int, architecture.split(':')))

        layers_binary, layer_counter = create_layers(neurons)

        create_semantics_io_files(neurons)
        filenames.append("input_semantics.csv")
        filenames.append("output_semantics.csv")

    # Write layers
    for i, layer in enumerate(layers_binary):
        hdf5_file_write(i, layer)

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
