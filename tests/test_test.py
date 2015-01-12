#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os
import tempfile
import json

# nntookit modules
import nntoolkit.test as test


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    test.get_parser()
