from game_2048 import Game
from random import choice
import numpy as np

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

movesEnv = ['up', 'down', 'left', 'right']

moves = [up, down, left, right]

game = Game(True)
game.reset()

# play the game with random moves until it's over
counter = 0
while game.valid():
    move = choice(moves)
    game.oneHotMove(move)
    print(movesEnv[np.argmax(move)])
    game.printBoard()
    counter += 1

game.printBoard()
print(game.score())
print("num steps: ", counter)