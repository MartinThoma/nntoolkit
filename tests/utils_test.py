#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import argparse
import os

# Third party modules
import pytest

# First party modules
import nntoolkit.utils as utils


def test_is_valid_file():
    parser = argparse.ArgumentParser()

    # Does exist
    path = os.path.realpath(__file__)
    assert utils.is_valid_file(parser, path) == path

    # Does not exist
    with pytest.raises(SystemExit):
        utils.is_valid_file(parser, "/etc/nonexistingfile")


def test_is_valid_folder():
    parser = argparse.ArgumentParser()

    # Does exist
    assert utils.is_valid_folder(parser, "/etc") == "/etc"

    # Does not exist
    with pytest.raises(SystemExit):
        utils.is_valid_folder(parser, "/etc/nonexistingfoler")
