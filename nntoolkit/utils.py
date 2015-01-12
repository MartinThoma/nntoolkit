#!/usr/bin/env python

"""Utility functions that can be used in multiple scripts."""

import os
import logging
import tempfile
import numpy
import math
import shutil
import sys

# Data formats
import tarfile
import h5py
import yaml
import csv


PY3 = sys.version > '3'

if not PY3:
    from future.builtins import open


def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file system."""
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def is_valid_folder(parser, arg):
    """Check if arg is a valid file that already exists on the file system."""
    arg = os.path.abspath(arg)
    if not os.path.isdir(arg):
        parser.error("The folder %s does not exist!" % arg)
    else:
        return arg


def get_activation(activation_str):
    """Return a function that works on a numpy array."""
    sigmoid = numpy.vectorize(lambda x: 1./(1+numpy.exp(-x)))
    if activation_str == 'sigmoid':
        return sigmoid
    elif activation_str == 'softmax':
        return lambda x: numpy.divide(numpy.exp(x), numpy.sum(numpy.exp(x)))


def get_outputs(output_file):
    """Parse ``output_file`` which is a csv file and defines the semantics of
    the output of a neural network.

    For example, output neuron 1 means class "0" in the MNIST classification
    task.
    """
    outputs = []
    mode = 'rt'
    arguments = {'newline': '', 'encoding': 'utf8'}
    with open(output_file, mode, **arguments) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            outputs.append(row[0])
    return outputs


def get_model(modelfile):
    """Check if ``modelfile`` is valid.
    :param modelfile: path to a model.tar file which describes a neural
        network.
    :returns: A dictionary which describes the model if everything seems to be
        fine. Return ``False`` if errors occur.
    """
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
    inputs = []

    # if sys.version_info.major < 3:
    #     mode = 'rb'
    #     arguments = {}
    # else:
    mode = 'rt'
    arguments = {'newline': '', 'encoding': 'utf8'}

    input_semantics_file = os.path.join(tarfolder, 'input_semantics.csv')
    with open(input_semantics_file, mode, **arguments) as csvfile:
        spamreader = csv.reader(csvfile, delimiter="\n", quotechar='"')
        for row in spamreader:
            inputs.append(row[0])
    outputs = get_outputs(os.path.join(tarfolder, 'output_semantics.csv'))
    model_yml['inputs'] = inputs
    model_yml['outputs'] = outputs

    # Cleanup
    shutil.rmtree(tarfolder)
    return model_yml


def get_data(data_file):
    """Get data as x and y numpy arrays for a tar archive.
    :param training_data: The path to a tar file
    :returns: Tuple (x, y), where y might be ``None`` in case of success or
              ``False`` in case of error
    """
    if not os.path.isfile(data_file):
        logging.error("File '%s' does not exist.", data_file)
        return False

    if not tarfile.is_tarfile(data_file):
        logging.error("'%s' is not a valid tar file.", data_file)
        return False

    with tarfile.open(data_file) as tar:
        filenames = tar.getnames()
        if 'x.hdf5' not in filenames:
            logging.error("'%s' does not have a x.hdf5.", data_file)
            return False
        tar.extractall()
        x = h5py.File('x.hdf5', 'r')['x.hdf5'].value

        if 'y.hdf5' in filenames:
            y = h5py.File('y.hdf5', 'r')['y.hdf5'].value
            y = y.reshape(len(y), 1)
        else:
            y = None

    for filename in filenames:
        # Cleanup
        os.remove(filename)

    return (x, y)


def write_model(model, model_file_path):
    """Write ``model`` to ``model_file_path``.
    :returns: False if it failed.
    """
    model_yml = {}
    model_yml['type'] = 'mlp'

    logging.info("Create %s...", model_yml['type'])

    filenames = ["model.yml", "input_semantics.csv", "output_semantics.csv"]

    # input_semantics
    with open("input_semantics.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter="\n",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for semantic in model['inputs']:
            spamwriter.writerow(semantic)

    # output_semantics
    with open("output_semantics.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter="\n",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for semantic in model['outputs']:
            spamwriter.writerow(semantic)

    # Write HDF5 files
    model_yml['layers'] = []
    for i, layer in enumerate(model['layers']):
        W, b = layer['W'], layer['b']
        model_yml['layers'].append({'W': {'size': list(W.shape),
                                          'filename': 'W%i.hdf5' % i},
                                    'b': {'size': list(b.shape),
                                          'filename': 'b%i.hdf5' % i},
                                    'activation': 'TODO'})
        # Write HDF5 files
        Wfile = h5py.File('W%i.hdf5' % i, 'w')
        Wfile.create_dataset(Wfile.id.name, data=W)
        Wfile.close()
        filenames.append('W%i.hdf5' % i)

        bfile = h5py.File('b%i.hdf5' % i, 'w')
        bfile.create_dataset(bfile.id.name, data=b)
        bfile.close()
        filenames.append('b%i.hdf5' % i)

    # Create YAML file
    with open("model.yml", 'w') as f:
        yaml.dump(model_yml, f, default_flow_style=False)

    # Create tar file
    with tarfile.open(model_file_path, "w:") as tar:
        for name in filenames:
            tar.add(name)

    # Remove temporary files which are now in tar file
    for filename in filenames:
        os.remove(filename)
