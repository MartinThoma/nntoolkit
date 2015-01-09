#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Train a neural network."""


import numpy as np
import tarfile
import logging
import os
import h5py

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
    parser.add_argument("-o", "--output",
                        dest="model_output_file",
                        help="""where should the new model be written?""",
                        metavar="FILE",
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
    parser.add_argument("--epochs",
                        dest="epochs",
                        help=("Positive number of training epochs"),
                        default=100,
                        type=int)
    return parser


def minibatch_gradient_descent(model,
                               x,
                               y,
                               batch_size=256,
                               lr=0.1,
                               epochs=100):
    """Train a given neural network.
    :param model: A parsed model
    :param x: A numpy array with features
    :param y: The list of classes
    :param batch_size: A positive integer which defines after how many training
    examples the values of the neural network get adjusted
    :param lr: Learning rate. Has to be positive.
    """
    assert lr > 0
    assert batch_size >= 1

    # See:
    # http://deeplearning.net/software/theano/cifarSC2011/introduction.html
    # http://deeplearning.net/tutorial/mlp.html

    # symbol declarations
    sx = tensor.matrix()
    sy = tensor.matrix()

    params_to_learn = []
    layers_shared = []
    for layer in model['layers']:
        W = theano.shared(np.array(layer['W'], dtype=theano.config.floatX))
        b = theano.shared(np.array(layer['b'], dtype=theano.config.floatX))
        layers_shared.append({'W': W, 'b': b})
        params_to_learn.append(W)
        params_to_learn.append(b)

    # symbolic expression-building
    last_output = sx
    for layer in layers_shared:
        W, b = layer['W'], layer['b']
        # TODO: Sigmoid - make dependant from activation function
        hid = tensor.tanh(tensor.dot(last_output, W) + b)
        last_output = hid
    out = last_output

    # Classification error
    err = 0.5 * tensor.sum(out - sy) ** 2

    # Build dictuionary of parameters which get updated
    u_params_to_learn = {}
    g_params_to_learn = tensor.grad(err, params_to_learn)
    for param, gparam in zip(params_to_learn, g_params_to_learn):
        u_params_to_learn[param] = param - lr * gparam

    # compile a fast training function
    train = theano.function([sx, sy],
                            err,
                            updates=u_params_to_learn)

    # now do the computations
    trainingloops = epochs * max(1, int(len(x) / batch_size))
    for i in range(trainingloops):
        print("Epoch %i" % i)
        x_i = x[i * batch_size: (i + 1) * batch_size]
        y_i = y[i * batch_size: (i + 1) * batch_size]
        print(x_i.shape)
        print(y_i.shape)
        err_i = train(x_i, y_i)
        logging.info("Loss %0.2f", err_i)


def get_data(data_file):
    """Get data as x and y numpy arrays for a tar archive.
    :param training_data: The path to a tar file
    :returns: Tuple (x, y), where y might be ``None`` in case of success or
              ``False`` in case of error
    """
    if not os.path.isfile(data_file):
        logging.error("File '%s' does not exist.", data_file)
        return False

    if not tarfile.is_tarfile(data_file):
        logging.error("'%s' is not a valid tar file.", data_file)
        return False

    with tarfile.open(data_file) as tar:
        filenames = tar.getnames()
        if 'x.hdf5' not in filenames:
            logging.error("'%s' does not have a x.hdf5.", data_file)
            return False
        tar.extractall()
        x = h5py.File('x.hdf5', 'r')['x.hdf5'].value

        if 'y.hdf5' in filenames:
            y = h5py.File('y.hdf5', 'r')['y.hdf5'].value
            y = y.reshape((len(y), 1))
        else:
            y = None

    return (x, y)


def main(model_file,
         model_output_file,
         training_data,
         batch_size,
         learning_rate,
         epochs):
    """Train model_file with training_data."""
    x, y = get_data(training_data)
    assert y is not None
    model = utils.get_model(model_file)
    minibatch_gradient_descent(model,
                               x, y,
                               batch_size,
                               learning_rate,
                               epochs)
    utils.write_model(model, model_output_file)

if __name__ == '__main__':
    args = get_parser().parse_args()
    main(args.model_file,
         args.model_output_file,
         args.training_data,
         args.batch_size,
         args.learning_rate,
         args.epochs)
