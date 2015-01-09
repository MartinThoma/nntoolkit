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


def main(nn_type, architecture, model_file):
    """Create a neural network file of ``nn_type`` with ``architecture``."""
    if os.path.isfile(model_file):
        logging.error("'%s' already exists.", model_file)
        return
    if not model_file.endswith(".tar"):
        logging.error("'%s' does not end with '.tar'.", model_file)
        return
    logging.info("Create %s with a %s architecture...", nn_type, architecture)

    filenames = ["model.yml"]  # "input_semantics.csv", "output_semantics.csv"

    if nn_type == 'mlp':
        # Create layers by looking at 'architecture'
        layers = []
        layers_binary = []

        # TODO: the activation function could be here!
        neurons = list(map(int, architecture.split(':')))

        for neurons_a, neurons_b in zip(neurons, neurons[1:]):
            # TODO: right order?
            W = [[random.random() for i in range(neurons_a)]
                 for j in range(neurons_b)]
            # TODO: neurons_a or b?
            b = [random.random() for i in range(neurons_a)]
            layers_binary.append({'W': numpy.array(W),
                                  'b': numpy.array(b),
                                  'activation': 'sigmoid'})  # TODO: activation

    # Write layers
    for i, layer in enumerate(layers_binary):
        Wfile = h5py.File('W%i.hdf5' % i, 'w')
        Wfile.create_dataset(Wfile.id.name, data=layer['W'])
        Wfile.close()

        bfile = h5py.File('b%i.hdf5' % i, 'w')
        bfile.create_dataset(bfile.id.name, data=layer['b'])
        bfile.close()

        layers.append({'W': {'size': list(layer['W'].shape),
                             'filename': 'W%i.hdf5' % i},
                       'b': {'size': list(layer['b'].shape),
                             'filename': 'b%i.hdf5' % i},
                       'activation': layer['activation']})
        filenames.append('W%i.hdf5' % i)
        filenames.append('b%i.hdf5' % i)

        model = {'type': 'mlp', 'layers': layers}

    with open("model.yml", 'w') as f:
        yaml.dump(model, f, default_flow_style=False)

    # Create tar file
    with tarfile.open("model.tar", "w:") as tar:
        for name in filenames:
            tar.add(name)

    # Remove temporary files which are now in tar file
    for filename in filenames:
        os.remove(filename)


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.type, args.architecture, args.model_file)
