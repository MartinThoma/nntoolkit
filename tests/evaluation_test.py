#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os
import tempfile
import json

# nntookit modules
import nntoolkit.evaluate as evaluate


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    evaluate.get_parser()


def simple_evluation_test():
    """Evaluate a model with a simple example feature vector."""
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model.tar")
    nose.tools.assert_equal(os.path.isfile(model_file), True)

    features = [0 for i in range(167)]

    evaluate.main(model_file, features)

    # Test the bash version
    fd, feature_file = tempfile.mkstemp('.json')
    with open(feature_file, "w") as outfile:
        json.dump(features, outfile)
    evaluate.main_bash(model_file, feature_file)
    os.remove(feature_file)


def non_existing_model_file_test():
    """Check what happens when a non-existing model file is given to the main
    evaluate method.
    """
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model-nonexistent.tar")
    features = [0 for i in range(167)]

    evaluation_result = evaluate.main(model_file, features)
    nose.tools.assert_equal([], evaluation_result)
    # TODO: Is that a good idea? This should probably rather return an error.


def non_tarfile_model_file_test():
    """Check what happens when a non-tarfile model file is given to the main
    evaluate method.
    """
    # Get model file
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "features.json")
    features = [0 for i in range(167)]

    evaluation_result = evaluate.main(model_file, features)
    nose.tools.assert_equal([], evaluation_result)
    # TODO: Is that a good idea? This should probably rather return an error.


def show_empty_results_test():
    """Show an empty results list."""
    print_string = evaluate.show_results([])
    nose.tools.assert_equal("-- No results --", print_string)
