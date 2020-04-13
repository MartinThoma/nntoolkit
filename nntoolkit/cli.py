#!/usr/bin/env python

# Core Library modules
import json
import logging
import os
import sys
from typing import Any, Dict

# Third party modules
import click
import tensorflow as tf

# First party modules
import nntoolkit.utils

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stderr,
)


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logger = logging.getLogger(__name__)
logging.getLogger("tensorflow").setLevel(logging.WARNING)
tf.get_logger().setLevel(logging.WARNING)


@click.group()
@click.version_option(version=nntoolkit.__version__)
def entry_point():
    """nntoolkit helps with neural network evaluation."""


model_option = click.option(
    "-m",
    "--model",
    "modelfile",
    help="where is the model file (.tar)?",
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
)


@entry_point.command()
@model_option
@click.option(
    "-i",
    "--input",
    "inputvec",
    help="a file which contains an input vector [[0.12, 0.312, 1.21 ...]]",
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
)
def evaluate(modelfile, inputvec):
    import nntoolkit.evaluate

    nntoolkit.evaluate.main_bash(modelfile, inputvec)


type_option = click.option(
    "-t",
    "--type",
    "nntype",
    type=click.Choice(["mlp"]),
    help="which type of neural network do you want to create?",
)


@entry_point.group()
def create():
    """Create a new model file."""


@create.command(name="mlp")
@click.argument("architecture")
@click.option(
    "-f",
    "--file",
    "model_file",
    help="write model file to MODEL_FILE (.tar)",
    default="nntoolkit-model.tar",
    type=click.Path(file_okay=True, dir_okay=False, exists=False, writable=True),
)
def create_mlp(architecture, model_file):
    """Create a multi-layer Perceptron architecture."""
    import nntoolkit.create

    nntoolkit.create.main(
        architecture=architecture, model_file=model_file, nn_type="mlp"
    )


@entry_point.command()
def make():
    """Deprecated. Use 'create' instead of 'make'."""
    print("Use 'create' instead of 'make'")


@entry_point.command()
@click.argument("traindata", required=True)
@click.argument("validdata", required=True)
@click.argument("testdata", required=True)
@click.option(
    "-m",
    "--model",
    "model_file",
    help="where is the model file (.tar) which should get trained?",
)
@click.option(
    "-o",
    "--output",
    "model_output_file",
    help="where should the new model be written?",
    type=click.Path(dir_okay=False, file_okay=True, exists=False),
    default=os.path.abspath("model.tar"),
)
@click.option(
    "--batchsize",
    "batch_size",
    help=(
        "A positive number which indicates how many "
        "training examples get looked at before the "
        "parameters get updated."
    ),
    type=int,
    default=256,
)
@click.option(
    "-lr",
    "--learning-rate",
    "learning_rate",
    help="A positive number, typically between 0 and 10.",
    type=float,
    default=0.1,
)
@click.option(
    "--epochs",
    "epochs",
    help="Positive number of training epochs",
    type=int,
    default=10,
)
@click.option(
    "--momentum",
    "momentum",
    help="A positive number, typically between 0 and 1.",
    type=float,
    default=0.1,
)
@click.option(
    "--hook", "hook", type=str,
)
def train(
    traindata,
    validdata,
    testdata,
    model_file,
    model_output_file,
    batch_size,
    learning_rate,
    epochs,
    momentum,
    hook,
):
    """Train a neural network."""
    import nntoolkit.train

    if model_file is None:
        model_dict: Dict[str, Any] = json.loads(input())
    else:
        model_dict: Dict[str, Any] = nntoolkit.utils.get_model(model_file)

    nntoolkit.train.main(
        model_dict=model_dict,
        model_output_file=model_output_file,
        training_data=traindata,
        batch_size=batch_size,
        learning_rate=learning_rate,
        epochs=epochs,
    )


@entry_point.command()
@model_option
@click.option(
    "-i",
    "--input",
    "test_data",
    help="a file which contains testing data (.tar)",
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
)
def test(model_file, test_data):
    """Test a neural network."""
    import nntoolkit.test

    nntoolkit.test.main(model_file, test_data)


if __name__ == "__main__":
    entry_point()
