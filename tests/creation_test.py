#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os
import tempfile
import json

# nntookit modules
import nntoolkit.create as create


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    create.get_parser()


def simple_creation_test():
    """Evaluate a model with a simple example feature vector."""
    # Get model file
    create.main("mlp", "10:12:8", "model_test.tar")


def create_already_exists_test():
    """Try to create a model 'over' a file which already exists."""
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model.tar")
    create.main("mlp", "10:12:8", model_file)
    # TODO: Check if error was logged


def create_nontar_model_test():
    """Try to create a model which has no tar file."""
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model-nonexistent.bla")
    create.main("mlp", "10:12:8", model_file)
    # TODO: Check if error was logged
