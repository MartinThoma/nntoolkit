#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os
import tempfile
import json

# nntookit modules
import nntoolkit.train as train


# Tests
def get_parser_test():
    """Check if the evaluation model returns a parser object."""
    train.get_parser()
