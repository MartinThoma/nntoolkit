#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a neural network model file."""

# Core Library modules
import logging
import os
import random
import tarfile
from typing import Any, Dict, List

# Third party modules
import h5py
import numpy
import yaml

# First party modules
import nntoolkit.utils

logger = logging.getLogger(__name__)


def xaviar10_weight_init(neurons_a: int, neurons_b: int):
    """Initialize the weights between a layer with ``neurons_a`` neurons
    and a layer with ``neurons_b`` neurons.

    Returns
    -------
    A neurons_a × neurons_b matrix.
    """
    fan_in = neurons_a
    fan_out = neurons_b - 2
    init_weight = 4.0 * numpy.sqrt(6.0 / (fan_in + fan_out))
    W = [
        numpy.random.uniform(low=-init_weight, high=init_weight, size=neurons_a)
        for _ in range(neurons_b)
    ]
    return W


def is_valid_model_file(model_file_path):
    """Check if `model_file_path` is a valid model file."""
    if os.path.isfile(model_file_path):
        logger.error("'%s' already exists.", model_file_path)
        return False
    if not model_file_path.endswith(".tar"):
        logger.error("'%s' does not end with '.tar'.", model_file_path)
        return False
    return True


def create_hdf5s_for_layer(i, layer):
    """Create one HDF5 file for the weight matrix W and one for the bias vector
    b.
    """
    Wfile = h5py.File("W%i.hdf5" % i, "w")
    Wfile.create_dataset(Wfile.id.name, data=layer["W"])
    Wfile.close()

    bfile = h5py.File("b%i.hdf5" % i, "w")
    bfile.create_dataset(bfile.id.name, data=layer["b"])
    bfile.close()


def create_layers(neurons: List[int]) -> List[Dict[str, Any]]:
    """
    Create the layers of the neural network.

    Parameters
    ----------
    neurons : List[int]
        Indicates how many neurons are in which layer.

    Returns
    -------
    layers_binary : List[Dict[str, Any]]
        random variables for the weight matrix W and the bias vector b
    """
    layers_binary = []
    for neurons_b, neurons_a in zip(neurons, neurons[1:]):
        W = xaviar10_weight_init(neurons_a, neurons_b)
        b = [random.random() for _ in range(neurons_a)]
        # TODO: parse architecture string to allow arbitrary activation
        # functions
        layers_binary.append(
            {
                "W": numpy.array(W, dtype=numpy.float32),
                "b": numpy.array(b, dtype=numpy.float32),
                "activation": "Sigmoid",
            }
        )
    layers_binary[-1]["activation"] = "Softmax"
    return layers_binary


def main(nn_type: str, architecture: str, model_file: str):
    """
    Create a neural network file of ``nn_type`` with ``architecture``.

    Store it in ``model_file``.

    Parameters
    ----------
    nn_type : {'mlp'}
    architecture: str
    model_file : str
        A path which should end with .tar. The created model will be written
        there.
    """
    if not is_valid_model_file(model_file):
        return

    logger.info("Create %s with a %s architecture...", nn_type, architecture)

    filenames = ["model.yml"]  # "input_semantics.csv", "output_semantics.csv"

    if nn_type == "mlp":
        # Create layers by looking at 'architecture'
        layers = []

        # TODO: the activation function could be here!
        neurons = list(map(int, architecture.split(":")))

        layers_binary = create_layers(neurons)

        nntoolkit.utils.create_boilerplate_semantics_files(neurons)
        filenames.append("input_semantics.csv")
        filenames.append("output_semantics.csv")

    # Write layers
    for i, layer in enumerate(layers_binary):
        create_hdf5s_for_layer(i, layer)

        layers.append(
            {
                "W": {"size": list(layer["W"].shape), "filename": "W%i.hdf5" % i},
                "b": {"size": list(layer["b"].shape), "filename": "b%i.hdf5" % i},
                "activation": layer["activation"],
            }
        )
        filenames.append("W%i.hdf5" % i)
        filenames.append("b%i.hdf5" % i)

        model = {"type": "mlp", "layers": layers}

    with open("model.yml", "w") as f:
        yaml.dump(model, f, default_flow_style=False)

    # Create tar file
    with tarfile.open(model_file, "w:") as tar:
        for name in filenames:
            tar.add(name)

    # Remove temporary files which are now in tar file
    for filename in filenames:
        os.remove(filename)
