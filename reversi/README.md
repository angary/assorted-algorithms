# Random notes from development process

## Kinda interesting notes
- Using a 2D numpy array for representation of the board was slower than using a 2D python list (maybe - MAYBE -  because when a new game was created all the values in the 2D list were initialised so they were all in a contiguous slab of memory, but I'm really not familiar with python memory management)
- Using small datatype sizes (i.e. numpy.int8) when initialising the numpy array for representation of the board resulted in even slower runtime than the original 2D numpy array with default data type
- A spreadsheet showcasing how many scenarios the minimax function would search each turn for different minimax search depths is linked [here](https://docs.google.com/spreadsheets/d/1Bg-CorpUQpmLuJNiVqcAQRPe22uGhv7ZhbHWpEP5OJg/edit?usp=sharing). Results are a bit scuffed - the algorithm also had alpha beta pruning, so it may explain why there would be an inconsistent increase in checks for different turns/ depth checks, but it didn't have a transposition table, so the time taken to run should be correlated to number of checks.

## Me complaining about my code
- Main limitation of algo is my implementation of the heuristics/ weights. The heuristics' inaccuracy also limits the potential of optimisations such as PVS/ iterative deepening.
- Negamax/ negascout wasn't implemented because sometimes a player can have multiple moves, and the algorithm would probably save 10 lines of code while introducing many more to consider what constitutes a 'turn'
- MCTS