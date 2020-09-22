<h1>Assorted Algorithms</h1>
A bunch of algorithms that I decided to showcase. If I'm currently working on something at the moment, the most recent commit will be in the dev branch. 
<br><br>



[true false practise](true_false_practise.py)</br>
First piece of code I uploaded to github in this previously private repo, held here for SenTimEnTaL vAluE.
<br><br>



[magic_knights_tour](magic_knights_tour.py)<br>
<b>Generates path for a knight at any starting point, so it reaches every square on a chess board once, and if we plot the turn when it reached a square, on that square of the board, the sum of turns on all rows and columns of the board is equal.</b>
<br>
Given a starting point, it uses a recursive backtracking solve involving regular quartes, Warnsdorff's heuristic and quad backtracking to generate a path.
<br><br>


[markov_chain_text](markov_chain_text.py)<br>
<b>Reads text file, and generates a new piece of text using the same immediate word probabilities.</b></br>
Generates a markov chain (weighted directed graph) from a given text, where each vertex is a word pointing to words that came after it in the text, with number of occurences as edge weight. The text is generated through a series of probablistic state transitions from each vertex.
<br><br>


[reversi](reversi)
<b>(Work in progress)</b><br>
<b>A command line implementation of the game 'Reversi' along with an AI to play against.</b></br>
Uses a minimax algorithm, with move sorting and alpha beta pruning. Heuristics includes - mobility, corners captured, frontier length, stability, and 'value' of a square. Extra optimisations - transposition table and zobrist keys.
