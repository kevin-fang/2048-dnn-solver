from random import choice, randint
import collections, copy
import numpy as np

zero = lambda x: True if x == 0 else False
possibleRandom = [2, 4]

# fill an empty space with the contents of the tiles after
# [4, 0, 0, 2] -> [4, 2, 0, 0]
# [4, 0, 2, 0] -> [4, 2, 0, 0]
def fillEmpty(row, givenIndex):
    fillIndex = givenIndex + 1
    if (fillIndex == len(row) - 1):
        return row
    counter = 0 # only allow it to loop to the end of the row
    while row[fillIndex] == 0 and counter < len(row):
        for i in range(fillIndex, len(row) - 1):
            row[i] = row[i + 1]
            row[i + 1] = 0
        counter += 1
    return row

# move a row left and merge everything
# [2, 2, 0, 0] -> [4, 0, 0, 0]
# [2, 2 ,2, 2] -> [4, 4, 0, 0]
# [0, 2, 2, 2] -> [4, 2, 0, 0]
def moveRowLeft(row):
    if row[0] == 0:
        row = fillEmpty(row, -1)
    for index, item in enumerate(row):
        if index < len(row) - 1:
            row = fillEmpty(row, index)
        # if the index is in the first, second, or third and there is a merge to be made, merge and fill
        if index < len(row) - 1 and item == row[index + 1] and not zero(item):
            row[index] *= 2
            row[index + 1] = 0
            row = fillEmpty(row, index)
    return row


class Game:
    testingBoard = [[0, 0, 0, 0], 
                     [0, 0, 0, 0], 
                     [0, 0, 4, 0], 
                     [0, 2, 0, 0]]

    # initialize with 4x4 board with two 2's randomly placed
    def __init__(self, testing=False, dieOnBadMove=False):
        # create 4x4 array of zeros
        self.board = [[0] * 4 for i in range(4)]

        # game starts with two 2's placed randomly on the board
        x1, y1 = randint(0, 3), randint(0, 3)
        x2, y2 = randint(0, 3), randint(0, 3)
        
        # change y position if both values are the same
        while x1 == x2 and y1 == y2:
            y1 = randint(0, 3)

        self.board[x1][y1] = choice(possibleRandom)
        self.board[x2][y2] = choice(possibleRandom)
        if (testing):
            self.board = self.testingBoard

        self.dieOnBadMove = dieOnBadMove # TODO: add dying immediately on bad move
        self.dead = False
    
    def reset(self):
        self.__init__()

    def flipBoard(self):
        board = self.board
        for index, row in enumerate(board):
            board[index] = row[::-1]
    
    def rotateCW(self):
        self.board = [list(a) for a in zip(*self.board[::-1])]
    
    def rotateCCW(self):
        for i in range(3):
            self.rotateCW()

    def printBoard(self):
        print('', self.board[0], '\n', self.board[1], '\n', self.board[2], '\n', self.board[3], '\n')
    

    def valid(self):
        if (self.dead):
            return False

        emptyVals = []
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val == 0:
                    emptyVals.append((x, y))
        if len(emptyVals) == 0:
            return False
        else:
            return True

    # adds a random 2 or 4 to the board
    def checkBoardAndAddRandomTile(self):
        emptyVals = []
        for x, row in enumerate(self.board):
            for y, val in enumerate(row):
                if val == 0:
                    emptyVals.append((x, y))
        if len(emptyVals) == 0:
            return False
        else:
            newCoords = choice(emptyVals)
            newVal = choice(possibleRandom)
            self.board[newCoords[0]][newCoords[1]] = newVal
            return True, newVal

    def score(self):
        score = 0
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                score += val
        return score

    def highest(self):
        highest = 0
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val > highest:
                    highest = val
        return highest

    # make a left move. Used for each other implementation
    def left(self):
        changed = False
        # copy the board
        old_board = copy.deepcopy(self.board)
        for index, row in enumerate(self.board):
            self.board[index] = moveRowLeft(row)
        gameValid, newVal = self.checkBoardAndAddRandomTile()
        if not gameValid:
            print("Game over. Score: " + self.score())
        return newVal, old_board != self.board

    # flip board, move left, and flip board again. Seems complicated but is actually the simplest way to implement
    # [2, 0, 0, 4] -> [4, 0, 0, 2] -> [4, 2, 0, 0] -> [0, 0, 2, 4]
    def right(self):
        self.flipBoard()
        newVal, moved = self.left()
        self.flipBoard()
        return newVal, moved

    # rotate rows counterclockwise, move left, and rotate rows clockwise
    def up(self):
        self.rotateCCW()
        newVal, moved = self.left()
        self.rotateCW()
        return newVal, moved
    
    # rotate rows clockwise, move left, and rotate rows counterclockwise
    def down(self):
        self.rotateCW()
        newVal, moved = self.left()
        self.rotateCCW()
        return newVal, moved

    # parse an array and make the appropriate move. For AI purposes.
    # [up, down, left, right]
    def oneHotMove(self, oneHotArray):
        if oneHotArray[0] == 1: 
            newVal, moved = self.up()
        elif oneHotArray[1] == 1:
            newVal, moved = self.down()
        elif oneHotArray[2] == 1:
            newVal, moved = self.left()
        elif oneHotArray[3] == 1:
            newVal, moved = self.right()

        
        observation = self.board
        total = self.score()
        reward = newVal if moved else 0
        valid = True if self.valid() else False
        return observation, total, reward, valid