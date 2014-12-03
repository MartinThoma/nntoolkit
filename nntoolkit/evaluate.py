#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Evaluate a neural network."""

import logging
import sys
import os
import yaml

# nntoolkit modules
import nntoolkit
import nntoolkit.utils as utils


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="modelfolder",
                        help="where is the model folder (with a info.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=utils.default_model())
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="""a JSON string [[{x: 123, y:42, time:1337}],
                                               [...],
                                               ...]""",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=utils.default_model())
    return parser


def main(modelfolder, inputjson):
    """Evaluate the model described in ``modelfolder`` with ``inputjson`` as
       input data."""
    pass


if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.modelfolder, args.input)
