# Some notes

## The setup
- [reversi.py](reversi.py) contains code which runs the game, and does the interfacing between the user, ai, and game.
- [game.py](game.py) contains the game class which holds information about the game state and methods for playing
- [computer.py](computer.py) contains the ai code which includes the algos, and heuristics

## Kinda interesting notes
- Using a 2D numpy array for representation of the board was slower than using a 2D python list. Before I discuss numpy's downsides, it's important to consider that numpy is great for scenarios such as number crunching but here's some explanation as to why it may have been slower in my scenario:
  - Accessing many different values inside a python list is faster than with a numpy array. This is because a python list is a list of pointers to objects and accessing a value in a list means returning the object pointed to by that list index, whereas in numpy arrays, it is a contiguous area in memory, but there is extra overhead in converting the integer stored at that index into a python object to be returned. Great stack overflow explanation [here](https://stackoverflow.com/questions/44224696/converting-numpy-array-to-a-set-takes-too-long/44226069#44226069).
  - Inefficient syntax - by using python syntax rather than numpy syntax, the python interpreter ends up doing the work and is unable to take advantage of the faster numpy c++ code.
	- Numpy offers SIMD (single instruction multiple data) vectorised operations of its arrays, i.e. ```numpy.sum()``` which offers the ability to sum values of an array quickly. However, if there are not many scenarios where you can take advantage of this, the value of numpy decreases due to slower access times.
    - A pretty trivial but interesting case is accessing values in a multi dimensional numpy array like ```arr[100][100]``` (normal python syntax) means that you are getting the array at the 100th index, and then getting the value at the 100th index of that. Compared to ```arr[100, 100]``` (numpy syntax), which directly gets the value at that index resulting in faster access times. Point is, I didn't know at the time you could index arrays like that, which slowed down my code - but numpy was still slower than normal python lists after changing access syntax. Stack overflow link with bytecode explanation [here](https://stackoverflow.com/questions/29281680/numpy-individual-element-access-slower-than-for-lists).
- Using small datatype sizes (i.e. numpy.int8) when initialising the numpy array for representation of the board resulted in even slower runtime than the original 2D numpy array with default data type (not sure why).
- A spreadsheet showcasing how many scenarios the minimax function checked each turn is linked [here](https://docs.google.com/spreadsheets/d/1Bg-CorpUQpmLuJNiVqcAQRPe22uGhv7ZhbHWpEP5OJg/edit?usp=sharing). Results are scuffed - algorithm at time of testing had alpha beta pruning, so it may explain why there were inconsistent increases in checks for different turns/ depths, but it didn't have a transposition table, so time taken should be correlated to number of checks.

## Me complaining about my code
- Main limitation of algo is my implementation of the heuristics/ weights. The heuristics' inaccuracy also limits the potential of optimisations such as PVS/ iterative deepening.
- Negamax/ negascout wasn't implemented because sometimes a player can have multiple moves, and the algorithm would probably save 10 lines of code while introducing many more to consider what constitutes a 'turn'.
- I recommend setting the search depth to at least 4.
- Heuristics are painful to do.
- MCTS
