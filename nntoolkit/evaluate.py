#!/usr/bin/env python

"""Evaluate a neural network."""

# Core Library modules
import json
import logging
from typing import Any, Dict, List

# Third party modules
import numpy as np

# First party modules
import nntoolkit.utils as utils

logger = logging.getLogger(__name__)


def show_results(results, n=10, print_results=True):
    """Show the top-n results of a classification."""
    # Print headline
    s = ""
    if len(results) == 0:
        s += "-- No results --"
    else:
        s += "{:18s} {:}\n".format("Class", "Prob")
        s += "#" * 50 + "\n"
        for entry in results:
            if n == 0:
                break
            else:
                n -= 1
            s += "{:18s} {:>7.4f}%\n".format(
                entry["semantics"], entry["probability"] * 100
            )
        s += "#" * 50
    if print_results:
        print(s)
    return s


def get_model_output(model_dict: Dict[str, Any], x: np.ndarray):
    """
    Get the model output.

    Parameters
    ----------
    model_dict : Dict[str, Any]
    x : np.ndarray

    Returns
    -------
    The output vector of the model
    """
    if model_dict["type"] == "mlp":
        for layer in model_dict["layers"]:
            b, W, activation = layer["b"], layer["W"], layer["activation"]
            x = np.dot(x, W)
            x = activation(x + b)
        x = x[0]
    # create_keras_model(model_dict)
    return x


def create_keras_model(model_dict):
    import keras
    from keras import layers
    import os

    print(model_dict["layers"][0]["W"].shape)
    input_dims = model_dict["layers"][0]["W"].shape[0]
    inputs = keras.Input(shape=(input_dims,), name="features")
    x = inputs
    for i, layer in enumerate(model_dict["layers"]):
        print(f"W.shape={layer['W'].shape}")
        if i + 1 == len(model_dict["layers"]):
            activation = "softmax"
        else:
            activation = "sigmoid"
        x = layers.Dense(len(layer["b"]), activation=activation)(x)

    model = keras.Model(inputs=inputs, outputs=x, name="3_layer_mlp")

    # Restore weights
    for i, layer in enumerate(model_dict["layers"]):
        model.layers[i + 1].set_weights([layer["W"], layer["b"]])

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    filepath = os.path.abspath("model.hdf5")
    model.save(filepath)
    print(f"Stored keras file at: {filepath}")
    logger.info(f"Stored keras file at: {filepath}")


def get_results(
    model_output: List[Any], output_semantics: List[Any]
) -> List[Dict[str, Any]]:
    """
    Get the prediction with semantics.

    Parameters
    ----------
    model_output : List[Any]
        A list of probabilities
    output_semantics : List[Any]
        A list of semantics

    Returns
    -------
    A list of dictionaries which have probability and semantics as keys.
    """
    results = []
    for symbolnr, prob in enumerate(model_output):
        results.append(
            {
                "symbolnr": symbolnr,
                "probability": prob,
                "semantics": output_semantics[symbolnr],
            }
        )
    results = sorted(results, key=lambda x: x["probability"], reverse=True)
    return results


def main(
    modelfile: str, features: List[float], print_results: bool = True
) -> List[Dict[str, Any]]:
    """
    Evaluate the model described in ``modelfile`` with ``inputvec`` as input
    data.

    Parameters
    ----------
    features : List[float]
    print_results : bool
        Print results if True. Always return results.

    Returns
    -------
    List of possible answers, reverse-sorted by probability.
    """
    model = utils.get_model(modelfile)
    if not model:
        return []
    x = np.array([features])
    model_output = get_model_output(model, x)
    results = get_results(model_output, model["outputs"])

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
