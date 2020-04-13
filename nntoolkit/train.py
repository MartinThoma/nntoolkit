#!/usr/bin/env python

"""Train a neural network."""


# Core Library modules
import logging
import os
from typing import Any, Dict, List

# Third party modules
import numpy as np
from keras import optimizers

# First party modules
import nntoolkit.utils as utils

logger = logging.getLogger(__name__)


def minibatch_gradient_descent(
    model_dict: Dict[str, Any],
    x: np.ndarray,
    y: List[Any],
    batch_size: int = 256,
    lr: float = 0.1,
    epochs: int = 100,
):
    """
    Train a given neural network.

    Parameters
    ----------
    model_dict : Dict[str, Any]
        The path to a parsed model
    x : np.ndarray
        contains features
    y : List[classes]
    batch_size : positive integer
        Defines after how many training examples the values of the neural
        network get adjusted
    lr : positive float
        Learning rate

    Returns
    -------
    model : Keras model

    Notes
    -----
    A model_dict looks like this:

    {
        "type": "mlp",
        "layers": [
            {
                "W": {
                    "size": [
                        161,
                        488
                    ],
                    "filename": "W0.hdf5"
                },
                "b": {
                    "size": [
                        488
                    ],
                    "filename": "b0.hdf5"
                },
                "activation": "Sigmoid"
            },
            {
                "W": {
                    "size": [
                        488,
                        38
                    ],
                    "filename": "W1.hdf5"
                },
                "b": {
                    "size": [
                        38
                    ],
                    "filename": "b1.hdf5"
                },
                "activation": "Softmax"
            }
        ]
    }
    """
    assert lr > 0
    assert batch_size >= 1

    for layer in model_dict["layers"]:
        assert os.path.isfile(layer["W"]["filename"])
        assert os.path.isfile(layer["b"]["filename"])

    model = create_mlp_from_dict(model_dict)
    optimizer = optimizers.SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer)

    y_cat = y.reshape(-1)
    model.fit(
        x, y_cat, epochs=epochs, batch_size=batch_size,
    )
    return model


def create_mlp_from_dict(model: Dict[str, Any]):
    """
    Create a multi-layer perceptron from a dictionary.

    Parameters
    ----------
    model : Dict[str, Any]

    Notes
    -----
    A model looks like this:

    {
        "type": "mlp",
        "layers": [
            {
                "W": {
                    "size": [
                        161,
                        488
                    ],
                    "filename": "W0.hdf5"
                },
                "b": {
                    "size": [
                        488
                    ],
                    "filename": "b0.hdf5"
                },
                "activation": "Sigmoid"
            },
            {
                "W": {
                    "size": [
                        488,
                        38
                    ],
                    "filename": "W1.hdf5"
                },
                "b": {
                    "size": [
                        38
                    ],
                    "filename": "b1.hdf5"
                },
                "activation": "Softmax"
            }
        ]
    }
    """
    from keras.models import Model
    from keras.layers import Input, Dense

    model_input = Input(shape=(model["layers"][0]["W"]["size"][0],))
    x = model_input
    for layer in model["layers"]:
        x = Dense(layer["b"]["size"][0])(x)
    model = Model(inputs=model_input, outputs=x)
    return model


def main(
    model_dict: Dict[str, Any],
    model_output_file: str,
    training_data: str,
    batch_size: int,
    learning_rate: float,
    epochs: int,
):
    """Train model_file with training_data."""
    data = utils.get_data(training_data)
    x, y = data
    assert y is not None

    model = minibatch_gradient_descent(
        model_dict, x, y, batch_size, learning_rate, epochs
    )
    utils.write_model(model_dict, model, model_output_file)
    logger.info(f"Saved model to {model_output_file}")
