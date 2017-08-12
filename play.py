from board import Board

def printBoard(game):
    print('', game.board[0], '\n', game.board[1], '\n', game.board[2], '\n', game.board[3], '\n')

up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

game = Board(True)
printBoard(game)
game.oneHotMove(left)
printBoard(game)
