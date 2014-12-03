A neural network can be stored in multiple files contained in a `tar` archive:

 - info.yml: A configuration file
 - Multiple HD5 files for matrices

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