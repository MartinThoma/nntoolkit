Multilayer Perceptrons
======================

    A multilayer perceptron (MLP) is a feedforward artificial neural network model that maps sets of input data onto a set of appropriate outputs.

Source: https://en.wikipedia.org/wiki/Multilayer_perceptron


Notation
--------

You can write the topology (architecture) of a MLP by writing down the number
of neurons per layer separated by ':'. Three examples are:

* ``160:10`` - A MLP with 160 input neurons (160 features) and 10 output neurons.
  It has no hidden layer(s).
* ``160:1337:456`` - A MLP with 160 input neurons, one hidden layer with 1337 neurons
  and 456 output neurons (classes)
* ``4:20:21:4`` - A MLP with 4 input neurons, 20 neurons in the first hidden layer
  and 21 in the second hidden layer. It has 4 output neurons.

If you want to show the activation function like this:

``(160,sigmoid):(500,sigmoid):(500,tanh):(369,softmax)``

If it is not noted otherwise, the activation function is always sigmoid and
in the last layer softmax.


Classification
--------------

Classification tasks can be tackled with MLPs by using one input neuron per
feature and one output neuron per class. For example, if you have a 28×28 pixel
image which is a digit (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), then you would make
a MLP with 28 · 28 = 784 input neurons and 10 output neurons.