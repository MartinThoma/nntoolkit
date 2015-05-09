#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Activation functions get applied within neural network nodes."""

import sys
import numpy
import logging
import inspect


def get_class(name, config_key, module):
    """Get the class by its name as a string.

    Parameters
    ----------
    name : string
        Name of the class
    config_key : string
        Name of the config key (if any) for the path to a plugin
    module :
        Module where to look for classes
    """
    clsmembers = inspect.getmembers(module, inspect.isclass)
    for string_name, act_class in clsmembers:
        if string_name == name:
            return act_class

    # Check if the user has specified a plugin and if the class is in there
    # cfg = get_project_configuration()
    # if config_key in cfg:
    #     modname = os.path.splitext(os.path.basename(cfg[config_key]))[0]
    #     if os.path.isfile(cfg[config_key]):
    #         usermodule = imp.load_source(modname, cfg[config_key])
    #         clsmembers = inspect.getmembers(usermodule, inspect.isclass)
    #         for string_name, act_class in clsmembers:
    #             if string_name == name:
    #                 return act_class
    #     else:
    #         logging.warning("File '%s' does not exist. Adjust ~/.hwrtrc.",
    #                         cfg['data_analyzation_plugins'])

    logging.debug("Unknown class '%s'.", name)
    return None


def get_activation_function(function_name):
    """Get an activation function object by its class name.

    Parameters
    ----------
    function_name : string
        Name of the activation function.

    Examples
    --------
    >>> get_activation_function('Sigmoid')
    SigmoidFunction
    """
    return get_class(name=function_name,
                     config_key='activation-functions',
                     module=sys.modules[__name__])()


# Only activation function classes follow
# Each activation function has to implement the __str__, __repr__ and
# __call__ functions
class Sigmoid(object):

    """The sigmoid function :math:`f(x) = 1/(1+e^{-x})`."""

    def __repr__(self):
        return "Sigmoid"

    def __str__(self):
        return "Sigmoid"

    def __call__(self, x):
        sigmoid = numpy.vectorize(lambda x: 1./(1+numpy.exp(-x)))
        return sigmoid(x)


class Softmax(object):

    """The softmax function."""

    def __repr__(self):
        return "Softmax"

    def __str__(self):
        return "Softmax"

    def __call__(self, x):
        softmax = lambda x: numpy.divide(numpy.exp(x), numpy.sum(numpy.exp(x)))
        return softmax(x)
