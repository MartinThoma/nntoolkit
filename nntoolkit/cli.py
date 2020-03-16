#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import logging
import sys

# Third party modules
import click

# First party modules
import nntoolkit

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)


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

architecture_option = click.option("-a", "--architecture",)

new_model_option = click.option(
    "-f", "--file", "model_file", help="write model file to MODEL_FILE"
)


@entry_point.command()
@type_option
@architecture_option
@new_model_option
def create(nntype, architecture, model_file):
    """Create a new model file."""
    import nntoolkit.create

    nntoolkit.create.main(nntype, architecture, model_file)


@entry_point.command()
@type_option
@architecture_option
@new_model_option
def make(nntype, architecture, model_file):
    """Alias for 'create'."""
    import nntoolkit.create

    nntoolkit.create.main(nntype, architecture, model_file)


@entry_point.command()
@click.option(
    "-m",
    "--model",
    "model_file",
    help="where is the model file (.tar) which should get trained?",
)
@click.option(
    "-i",
    "--input",
    "training_data",
    help="a file which contains training data (.tar)",
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
)
@click.option(
    "-o",
    "--output",
    "model_output_file",
    help="where should the new model be written?",
    type=click.Path(dir_okay=False, file_okay=True, exists=False),
)
@click.option(
    "--batchsize",
    "model_output_file",
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
    "--learningrate",
    "model_output_file",
    help="A positive number, typically between 0 and 10.",
    type=float,
    default=0.1,
)
@click.option(
    "--epochs",
    "epochs",
    help="Positive number of training epochs",
    type=float,
    default=0.1,
)
def train(
    model_file, training_data, model_output_file, batch_size, learning_rate, epochs
):
    """Train a neural network."""
    import nntoolkit.train

    nntoolkit.train.main(
        model_file, model_output_file, training_data, batch_size, learning_rate, epochs,
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
