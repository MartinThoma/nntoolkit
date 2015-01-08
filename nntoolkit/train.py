#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Train a neural network."""


import numpy as np

import theano
import theano.tensor as tensor

# nntoolkit modules
import nntoolkit.utils as utils


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model_file",
                        help="where is the model file (.tar) which should get "
                             "trained?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    parser.add_argument("-i", "--input",
                        dest="training_data",
                        help="""a file which contains training data (.tar)""",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        required=True)
    parser.add_argument("--batchsize",
                        dest="batch_size",
                        help=("A positive number which indicates how many "
                              "training examples get looked at before the "
                              "parameters get updated."),
                        default=256,
                        type=int)
    parser.add_argument("-lr", "--learningrate",
                        dest="learning_rate",
                        help=("A positive number, typically between 0 and "
                              "10."),
                        default=0.1,
                        type=float)
    return parser


def minibatch_gradient_descent(model_file,
                               x,
                               y,
                               batch_size=256,
                               lr=0.1):
    """Train a given neural network.
    :param model_file: Path to the model.tar
    :param x: A numpy array with features
    :param y: The list of classes
    :param batch_size: A positive integer which defines after how many training
    examples the values of the neural network get adjusted
    :param lr: Learning rate. Has to be positive.
    """
    assert lr > 0
    assert batch_size >= 1
    # TODO: Create training code
    # See:
    # http://deeplearning.net/software/theano/cifarSC2011/introduction.html
    #########################
    # Theano for Training a
    # Neural Network on MNIST
    #########################

    # symbol declarations
    sx = tensor.matrix()
    sy = tensor.matrix()
    w = theano.shared(np.random.normal(avg=0, std=.1,
                                       size=(784, 500)))
    b = theano.shared(np.zeros(500))
    v = theano.shared(np.zeros((500, 10)))
    c = theano.shared(np.zeros(10))

    # symbolic expression-building
    hid = tensor.tanh(tensor.dot(sx, w) + b)
    out = tensor.tanh(tensor.dot(hid, v) + c)
    err = 0.5 * tensor.sum(out - sy) ** 2
    gw, gb, gv, gc = tensor.grad(err, [w, b, v, c])

    # compile a fast training function
    train = theano.function([sx, sy],
                            err,
                            updates={w: w - lr * gw,
                                     b: b - lr * gb,
                                     v: v - lr * gv,
                                     c: c - lr * gc})

    # now do the computations
    for i in range(1000):
        x_i = x[i * batch_size: (i + 1) * batch_size]
        y_i = y[i * batch_size: (i + 1) * batch_size]
        err_i = train(x_i, y_i)
        print(err_i)  # Loss - don't print always

    # TODO: Update parameters, save it?


def get_data(training_data):
    """Get data as x and y numpy arrays
    :param training_data: The path to a tar file
    """
    # TODO: Fill x and y with data from tar / HDF5 files
    x = np.array([])
    y = np.array([])
    return (x, y)


def main(model_file, training_data, batch_size, learning_rate):
    """Train model_file with training_data."""
    x, y = get_data(training_data)
    minibatch_gradient_descent(model_file, x, y, batch_size, learning_rate)

if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.model_file,
         args.training_data,
         args.batch_size,
         args.learning_rate)
