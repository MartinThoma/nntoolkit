#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Train a neural network."""


import numpy as np
import logging

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

    Parameters
    ----------
    model : A parsed model
    x : A numpy array with features
    y : The list of classes
    batch_size : positive integer
        Defines after how many training examples the values of the neural
        network get adjusted
    lr : positive float
        Learning rate
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
    for i, layer in enumerate(model['layers']):
        W = np.array(layer['W'], dtype=theano.config.floatX)
        W = theano.shared(W, name='W%i' % i)
        b = np.array(layer['b'], dtype=theano.config.floatX)
        b = b.reshape((1, len(b)))
        b = theano.shared(b, name='b%i' % i)
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
    out = tensor.argmax(last_output, axis=1)

    # Classification error
    err = 0.5 * tensor.sum(tensor.neq(out, sy)) ** 2

    # Build dictuionary of parameters which get updated
    u_params_to_learn = []
    g_params_to_learn = tensor.grad(cost=err, wrt=params_to_learn)
    for param, gparam in zip(params_to_learn, g_params_to_learn):
        u_params_to_learn.append((param, param - lr * gparam))

    # compile a fast training function
    train = theano.function(inputs=[sx, sy],
                            outputs=err,
                            updates=u_params_to_learn,
                            allow_input_downcast=True)

    # now do the computations
    loops_per_epoch = max(1, int(len(x) / batch_size))
    logging.debug("batch_size: %i", batch_size)
    logging.debug("Loops per epoch: %i", loops_per_epoch)
    trainingloops = epochs * loops_per_epoch
    for i in range(trainingloops):
        start = (i * batch_size) % len(x)
        end = ((i + 1) * batch_size) % len(x)
        if start > end:
            continue  # TODO: Eventually we miss training examples!
        x_i = x[start:end]
        y_i = y[start:end]
        err_i = train(x_i, y_i)
        #if i % loops_per_epoch == 0:
        print("Epoch %i/%i, Loss %0.2f" % (i+1, i / loops_per_epoch, err_i))


def main(model_file,
         model_output_file,
         training_data,
         batch_size,
         learning_rate,
         epochs):
    """Train model_file with training_data."""
    data = utils.get_data(training_data)
    if data is None:
        logging.error("Data could not be loaded. Stop training.")
        return
    x, y = data
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
