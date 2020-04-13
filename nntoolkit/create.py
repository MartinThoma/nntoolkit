#!/usr/bin/env python

"""Create a neural network model file."""

# Core Library modules
import json
import logging
import os
import random
from typing import Any, Dict, List

# Third party modules
import h5py
import numpy
import yaml

# First party modules
import nntoolkit.utils

logger = logging.getLogger(__name__)


def xaviar10_weight_init(neurons_a: int, neurons_b: int) -> List[List[float]]:
    """
    Initialize the weights between a layer with ``neurons_a`` neurons and a
    layer with ``neurons_b`` neurons.

    Returns
    -------
    W : List[List[float]]
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


def is_valid_model_file(model_file_path: str) -> bool:
    """Check if `model_file_path` is a valid model file."""
    if os.path.isfile(model_file_path):
        logger.error(f"'{model_file_path}' already exists.")
        return False
    if not model_file_path.endswith(".tar"):
        logger.error(f"'{model_file_path}' does not end with '.tar'.")
        return False
    return True


def create_hdf5s_for_layer(i: int, layer: Dict[str, Any]):
    """
    Create one HDF5 file for the weight matrix W and one for the bias vector b.

    Parameters
    ----------
    i : int
    layer : Dict[str, Any]
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
    nn_type : {"mlp"}
    architecture: str
        For nn_type = "mlp", this should be something like "100:256:10"
    model_file : str
        A path which should end with .tar. The created model will be written
        there.
    """
    if not is_valid_model_file(model_file):
        return

    logger.info("Create %s with a %s architecture...", nn_type, architecture)

    filenames = ["model.yml"]

    if nn_type == "mlp":
        # Create layers by looking at 'architecture'
        layers = []

        # TODO: the activation function could be here!
        neurons = list(map(int, architecture.split(":")))

        layers_binary = create_layers(neurons)

        nntoolkit.utils.create_boilerplate_semantics_files(neurons)
        filenames.append("input_semantics.csv")
        filenames.append("output_semantics.csv")
    else:
        raise NotImplementedError(
            f"nn_type='{nn_type}'' is not implmented. "
            f"Only nn_type='mlp' is implmented so far."
        )

    # Write layers
    for i, layer in enumerate(layers_binary):
        create_hdf5s_for_layer(i, layer)

        layers.append(
            {
                "W": {
                    "size": list(layer["W"].shape),
                    "filename": os.path.abspath(f"W{i}.hdf5"),
                },
                "b": {
                    "size": list(layer["b"].shape),
                    "filename": os.path.abspath(f"b{i}.hdf5"),
                },
                "activation": layer["activation"],
            }
        )
        filenames.append(os.path.abspath(f"W{i}.hdf5"))
        filenames.append(os.path.abspath(f"b{i}.hdf5"))

        model = {
            "type": "mlp",
            "layers": layers,
            "inputs": [f"input {i}" for i in range(neurons[0])],
            "outputs": [f"output {i}" for i in range(neurons[-1])],
        }

    with open("model.yml", "w") as f:
        yaml.dump(model, f, default_flow_style=False)
        print(json.dumps(model))

    # ATTENTION: The following was a good thought, but probably not done in the
    # master thesis. For this reason, it is left here as a comment.
    # Instead, the modelinfo.json file was always piped into nntoolkit.
    # This is a bad interface as multiple files lie around the project.
    # The two better options would be:
    # (1) Include everythin in one hdf5 file like keras does
    # (2) Add the files in a .tar file
    # Create tar file
    # with tarfile.open(model_file, "w:") as tar:
    #     for name in filenames:
    #         tar.add(name)

    # Remove temporary files which are now in tar file
    # for filename in filenames:
    #     os.remove(filename)
