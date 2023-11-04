v0.2.0
Tetravex Solver

I've been playing the Gnome version of Tetravex a lot recently and decided I wanted to write a
Tetravex solving algorithm. This project does not have a GUI or a playable version of the game
Tetravex. It does include an entire python implementation of the data structures needed to play
and solve Tetravex. You can generate a random puzzle of any size, shuffle that puzzle and write 
it to a file. 

You can also load puzzles from a file, and solve them.solve puzzles, and read them from a file.
To solve a Tetravex puzzle run 
$ python3 tetravex.py path/to/your/file.txt

If the input file contains the format detailed in docs/API.txt for the write_tetra_to_file() function then your puzzle should be solved.

If you have read this far you are probably interested in developing a Tetravex solver of your own
so I have tried hard to document my entire API in docs/API.txt. This project is licensed under
GPLv3 feel free to use any of the code provided in accordance with that license. 

If you write a python project that can read Tetravex tiles and identify the state of a Tetravex
board, then you could use this Tetravex solver on those board states.

It would also be cool to make a version of this that can interact with the Gnome version of Tetravex
and enter the correct solution for you. This would allow you to get a really good time. 

Right now one would need to manually convert a puzzle state into python compatible data and then they
would have to manually enter the python solution. All that typing totally kills the time attack!

