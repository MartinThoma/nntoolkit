## Run this

```bash
$ ./get_data.py
$ nntoolkit create -t mlp -a 784:100:10 -f mnist_classifier.tar
$ nntoolkit test -m mnist_classifier.tar -i mnist_testdata.tar
$ nntoolkit train -m mnist_classifier.tar -i mnist_traindata.tar -o mnist_trained_classifier.tar
```