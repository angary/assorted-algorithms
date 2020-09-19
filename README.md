# Assorted Algorithms
A bunch of algorithms that I decided to showcase. If I'm currently working on something at the moment, the most recent commit will be in the dev branch. 
<br><br>



<h2>true false practise</h2><b>Oct 2019</b></br>
First piece of code I uploaded to github in this previously private repo, held here for SenTimEnTaL vAluE.
<br><br>



<h2>magic_knights_tour</h2><b>Aug 2020</b></br>
Generates a path for a knight from any starting point such that it reaches every square on a chess board once, and ensures that if we were to plot the turn that it reached the square on the square of the chess board, the sum of the turns on every row and column of the chess board is equal
<br><br>

*Given a starting point, it uses a recursive backtracking solve involving regular quartes, Warnsdorff's heuristic and quad backtracking to generate a path.*
<br><br>



<h2>markov_chain_text</h2><b>Sep 2020</b><br>
Reads a text file, and then generates a new piece of text using the same immediate word probabilities of the original text.
<br><br>

*Generates a markov chain (weighted directed graph) from a given text, where each vertex is a word pointing to words that came after it in the text, with number of occurences as edge weight. The text is generated through a series of probablistic state transitions from each vertex.*
<br><br>



<h2>reversi</h2><b>Sep 2020 (Work in progress)</b><br>
An basic command line implementation of the game 'Reversi' along with an AI to play against.
<br><br>

*Command line game with an AI opponent which uses a minimax algorithm, with move sorting and alpha beta pruning. Heuristics used includes - mobility, corners captured, frontier length, stability, and 'value' of a square. Extra optimisations - transposition table.*
