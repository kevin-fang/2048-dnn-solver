from board import Board
from random import choice

def printBoard(game):
    print('', game.board[0], '\n', game.board[1], '\n', game.board[2], '\n', game.board[3], '\n')

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

moves = [up, down, left, right]

game = Board(True)
printBoard(game)

# play the game with random moves until it's over
while game.gameValid():
    move = choice(moves)
    game.oneHotMove(move)
    printBoard(game)
