A neural network can be stored in multiple files contained in a `tar` archive:

 - model.yml: A configuration file that defines the model
 - Multiple HD5 files for matrices that countain parameters
 - input_semantics.csv: A file which has as many lines as the model has
   inputs. Each line gives clues for the meaning of the input
 - output_semantics.csv: A file which has as many lines as the model has
   outputs. Each line gives clues for the meaning of the output. In case of
   a classifier each output might correspond to a class. Then each line would
   have the name of the corresponding class.

## Structure of info.yml

```yml
type: mlp
layers:
  - b:
    - filename: 'b1.hd5'
    - size: 300
    W:
    - filename: 'W1.hd5'
    - size: (300, 500)
    activation: sigmoid
  - b:
    - filename: 'b2.hd5'
    - size: 500
    W:
    - filename: 'W2.hd5'
    - size: (500, 500)
    activation: logreg
```
