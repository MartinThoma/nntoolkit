#!/usr/bin/env python
# -*- coding: utf-8 -*-

# First party modules
import nntoolkit.train as train


def test_get_parser():
    """Check if the evaluation model returns a parser object."""
    train.get_parser()
