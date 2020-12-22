# Some notes

## The setup
- [main.py](main.py) contains the code to take in an input of a matrix, and prints out the factors
- [matrix_factorisation](matrix_factorisation.py) contains the actual matrix factorisation code

## Kinda interesting notes
- It's implemented in vanilla python to remove layers of abstraction and reveal what's actually going on, hence I wouldn't recommend using the raw code. Certain optimisations have been implemented for the sake of experimentation however, if you're looking for a proper version, just use sklearn
- Ideally the inputs for the input matrix are numbers close to each other, i.e. numbers in the range from 0 - 10, it goes a bit spastic 