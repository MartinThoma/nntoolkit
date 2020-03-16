#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import json
import os
import tempfile

# First party modules
import nntoolkit.evaluate as evaluate


# Tests
def test_get_parser():
    """Check if the evaluation model returns a parser object."""
    evaluate.get_parser()


def test_simple_evluation():
    """Evaluate a model with a simple example feature vector."""
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model.tar")
    assert os.path.isfile(model_file)

    features = [0 for i in range(167)]

    evaluate.main(model_file, features)

    # Test the bash version
    fd, feature_file = tempfile.mkstemp(".json")
    with open(feature_file, "w") as outfile:
        json.dump(features, outfile)
    evaluate.main_bash(model_file, feature_file)
    os.remove(feature_file)


def test_non_existing_model_file():
    """Check what happens when a non-existing model file is given to the main
    evaluate method.
    """
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model-nonexistent.tar")
    features = [0 for i in range(167)]

    evaluation_result = evaluate.main(model_file, features)
    assert evaluation_result == []
    # TODO: Is that a good idea? This should probably rather return an error.


def test_non_tarfile_model_file():
    """Check what happens when a non-tarfile model file is given to the main
    evaluate method.
    """
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "features.json")
    features = [0 for i in range(167)]

    evaluation_result = evaluate.main(model_file, features)
    assert evaluation_result == []
    # TODO: Is that a good idea? This should probably rather return an error.


def test_show_empty_results():
    """Show an empty results list."""
    print_string = evaluate.show_results([])
    assert print_string == "-- No results --"
