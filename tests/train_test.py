#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import json
import os
import tempfile

# First party modules
import nntoolkit.train as train
import nose


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    train.get_parser()
