#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os

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
