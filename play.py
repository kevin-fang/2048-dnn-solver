from board import Board

def printBoard(game):
    print('', game.board[0], '\n', game.board[1], '\n', game.board[2], '\n', game.board[3], '\n')

game = Board(True)
printBoard(game)
game.right()
printBoard(game)
