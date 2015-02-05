## Run this

```bash
tests/mnist$ ./get_data.py
[...]

tests/mnist$ nntoolkit create -t mlp -a 784:100:10 -f mnist_classifier.tar
2015-02-05 21:11:09,868 INFO Create mlp with a 784:100:10 architecture...

tests/mnist$ nntoolkit test -m mnist_classifier.tar -i mnist_testdata.tar
Correct: 1234/10000 = 0.12 of total correct

tests/mnist$ nntoolkit train -m mnist_classifier.tar -i mnist_traindata.tar -o mnist_classifier.tar --epochs 1 -lr 10 --batchsize 1
[...]

tests/mnist$ nntoolkit test -m mnist_classifier.tar -i mnist_testdata.tar
Correct: 2345/10000 = 0.23 of total correct
```