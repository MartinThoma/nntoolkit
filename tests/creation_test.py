#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import os

# First party modules
import nntoolkit.create as create


def test_simple_creation():
    """Evaluate a model with a simple example feature vector."""
    # Get model file
    create.main("mlp", "10:12:8", "model_test.tar")


def test_create_already_exists():
    """Try to create a model 'over' a file which already exists."""
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model.tar")
    create.main("mlp", "10:12:8", model_file)
    # TODO: Check if error was logged


def test_create_nontar_model():
    """Try to create a model which has no tar file."""
    current_folder = os.path.dirname(os.path.realpath(__file__))
    misc_folder = os.path.join(current_folder, "misc")
    model_file = os.path.join(misc_folder, "model-nonexistent.bla")
    create.main("mlp", "10:12:8", model_file)
    # TODO: Check if error was logged
