# Hardison Chess Python App

So I have been interested in Chess for a while now, and thought it would be a fun project to make a small chess engine. Here is a chess game you can play against the 'computer' (chess.com elo around 700).

#### Script BreakDown

##### Chess

Chess.py is what you should run if you want to play the computer. This is where the rendering of the board, the movement of the pieces, and all the other UI jazz happens.

##### ChessEngine

ChessEngine.py is where all the logic of the game exists. Where moves are tracked, where moves are checked to see if they are legal, and other logic,

##### ChessAI

ChessAI.py is where all the 'computer' logic is. This is where the computer evaluates the position, search through moves, and ultimately picks its best move

#### About the computer

The 'computer' uses a search tree, MiniMax Algorithm and Alpha Beta Pruning to pick the best moves. Currently the depth is set to look two moves in advance, mainly because its very slow. But you can set it to three or four moves but it might take some time.
