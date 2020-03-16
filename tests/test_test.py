#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import json
import os
import tempfile

# First party modules
import nntoolkit.test as test
import nose


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    test.get_parser()
