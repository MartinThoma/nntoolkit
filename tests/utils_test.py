#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import argparse
import os

# First party modules
import mock
import nntoolkit
import nntoolkit.utils as utils
import nose

# Tests
# @nose.tools.raises(SystemExit)
# def parser_test():
#     from argparse import ArgumentParser
#     parser = ArgumentParser()
#     home = os.path.expanduser("~")
#     rcfile = os.path.join(home, ".nntoolkitrc")
#     parser.add_argument("-m", "--model",
#                         dest="model",
#                         type=lambda x: utils.is_valid_folder(parser, x))
#     parser.parse_args(['-m', home])

#     parser = ArgumentParser()
#     parser.add_argument("-m", "--model",
#                         dest="model",
#                         type=lambda x: utils.is_valid_file(parser, x))
#     parser.parse_args(['-m', rcfile])


@nose.tools.raises(SystemExit)
def is_valid_file_test():
    parser = argparse.ArgumentParser()

    # Does exist
    path = os.path.realpath(__file__)
    nose.tools.assert_equal(utils.is_valid_file(parser, path), path)

    # Does not exist
    utils.is_valid_file(parser, "/etc/nonexistingfile")


@nose.tools.raises(SystemExit)
def is_valid_folder_test():
    parser = argparse.ArgumentParser()

    # Does exist
    nose.tools.assert_equal(utils.is_valid_folder(parser, "/etc"), "/etc")

    # Does not exist
    utils.is_valid_folder(parser, "/etc/nonexistingfoler")
