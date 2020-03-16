#!/usr/bin/env python

# Core Library modules
import gzip
import logging
import os
import sys
import tarfile
import tempfile
import urllib
from struct import unpack

# First party modules
import h5py
from numpy import uint8, zeros

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)



def get_labeled_data(imagefile, labelfile):
    """Read input-vector (image) and target class (label, 0-9) and return
       it as list of tuples.

    Parameters
    ----------
    imagefile : The file which contains the pixel information
    labelfile : The file which contains the labels

    Returns
    -------
    (xs, ys)
    """
    # Open the images with gzip in read binary mode
    images = gzip.open(imagefile, "rb")
    labels = gzip.open(labelfile, "rb")

    # Read the binary data

    # We have to get big endian unsigned int. So we need '>I'

    # Get metadata for images
    images.read(4)  # skip the magic_number
    number_of_images = images.read(4)
    number_of_images = unpack(">I", number_of_images)[0]
    rows = images.read(4)
    rows = unpack(">I", rows)[0]
    cols = images.read(4)
    cols = unpack(">I", cols)[0]

    # Get metadata for labels
    labels.read(4)  # skip the magic_number
    N = labels.read(4)
    N = unpack(">I", N)[0]

    if number_of_images != N:
        raise Exception("number of labels did not match the number of images")

    # Get the data
    x = zeros((N, rows, cols), dtype=uint8)  # Initialize numpy array
    y = zeros((N, 1), dtype=uint8)  # Initialize numpy array
    for i in range(N):
        if i % 1000 == 0:
            print("i: %i" % i)
        for row in range(rows):
            for col in range(cols):
                tmp_pixel = images.read(1)  # Just a single byte
                tmp_pixel = unpack(">B", tmp_pixel)[0]
                x[i][row][col] = tmp_pixel
        tmp_label = labels.read(1)
        y[i] = unpack(">B", tmp_label)[0]
    x = x.reshape(len(x), 28 * 28)
    return (x, y)


def create_nntoolkit_file(x, y, target_path):
    assert target_path.endswith(".tar")
    filenames = []

    train = h5py.File("x.hdf5", "w")
    train.create_dataset("x.hdf5", data=x)
    train.close()
    filenames.append("x.hdf5")

    train = h5py.File("y.hdf5", "w")
    train.create_dataset("y.hdf5", data=y)
    train.close()
    filenames.append("y.hdf5")

    # Create tar file
    with tarfile.open(target_path, "w:") as tar:
        for name in filenames:
            tar.add(name)

    # Remove temporary files which are now in tar file
    for filename in filenames:
        os.remove(filename)


def main():
    train = [
        "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    ]
    test = [
        "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
        "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
    ]

    # Download all files
    logging.info("Download all files")
    for url_path in train + test:
        filename = os.path.basename(url_path)
        if not os.path.isfile(filename):
            urllib.urlretrieve(url_path, filename)
    train = [os.path.basename(url_path) for url_path in train]
    test = [os.path.basename(url_path) for url_path in test]

    # Get strucutred data
    logging.info("Get strucutred data")
    x_train, y_train = get_labeled_data(train[0], train[1])
    x_test, y_test = get_labeled_data(test[0], test[1])

    # Create nntoolkits data file format
    logging.info("Create nntoolkits data file format")
    create_nntoolkit_file(x_test, y_test, "mnist_testdata.tar")
    create_nntoolkit_file(x_train, y_train, "mnist_traindata.tar")


if __name__ == "__main__":
    main()
