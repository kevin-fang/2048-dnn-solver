from game_2048 import Game

game = Game()
game.reset()
game.printBoard()
while game.valid():
    move = input('input move (left, right, up, down): ')
    if move == 'left':
        game.left()
    elif move == 'right':
        game.right()
    elif move == 'up':
        game.up()
    elif move == 'down':
        game.down()

    game.printBoard()