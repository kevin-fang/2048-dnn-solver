from random import choice, randint
import collections, copy
import numpy as np

zero = lambda x: True if x == 0 else False

# one hot elements
up = [1, 0, 0, 0]
down = [0, 1, 0, 0]
left = [0, 0, 1, 0]
right = [0, 0, 0, 1]

movesEnglish = ['up', 'down', 'left', 'right']
moves = [up, down, left, right]

# possibility of generating a 4 is 10%
possibleRandom = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]

class Game:
    # we use '0's to represent empty values
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
    
    # fill an empty space with the contents of the tiles after
    # [4, 0, 0, 2] -> [4, 2, 0, 0]
    # [4, 0, 2, 0] -> [4, 2, 0, 0]
    def fillEmpty(self, row, givenIndex):
        # given index is the index that was changed/moved. We want to fill the zero after that.
        fillIndex = givenIndex + 1
        if (fillIndex == len(row) - 1): # ignore if last element
            return row
        counter = 0 # only allow it to loop to the end of the row
        # if there is a zero and we haven't hit the counter max, run
        while row[fillIndex] == 0 and counter < len(row): 
            # loop until the end and copy the array one item to the left.
            for i in range(fillIndex, len(row) - 1):
                row[i] = row[i + 1]
                row[i + 1] = 0
            counter += 1
        return row

    # move a row left and merge everything
    # [2, 2, 0, 0] -> [4, 0, 0, 0]
    # [2, 2 ,2, 2] -> [4, 4, 0, 0]
    # [0, 2, 2, 2] -> [4, 2, 0, 0]
    def moveRowLeft(self, row):
        # just move everything to the left if the leftmost element is 0
        if row[0] == 0:
            row = self.fillEmpty(row, -1)
        
        # for the rest of the row, merge.
        for index, item in enumerate(row):
            # fill any empty spaces if needed.
            if index < len(row) - 1:
                row = self.fillEmpty(row, index)

            # if the index is in the first, second, or third and there is a merge to be made, merge and fill empty spaces
            if index < len(row) - 1 and item == row[index + 1] and not zero(item):
                row[index] *= 2
                row[index + 1] = 0
                row = self.fillEmpty(row, index)
        return row

    # reset the game with a random board
    def reset(self):
        self.__init__()

    # perform a mirror flip of the board
    def flipBoard(self):
        board = self.board
        for index, row in enumerate(board):
            board[index] = row[::-1]
    
    # rotate clockwise and counterclockwise - self explanatory (counterclockwise is 3x clockwise)
    def rotateCW(self):
        self.board = [list(a) for a in zip(*self.board[::-1])]
    def rotateCCW(self):
        for i in range(3):
            self.rotateCW()

    # print a nicely formatted copy of the board
    def printBoard(self):
        print('', self.board[0], '\n', self.board[1], '\n', self.board[2], '\n', self.board[3], '\n')

    # returns if the board is valid, i.e., there are some empty spaces on the board
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

    # scales the board so everything is log_2 of the item divided by the log_2(max_item). Used for AI purposes.
    def scale(self, board):
        #print(board)
        maxVal = np.amax(board)
        board = np.log2(board)
        board[board == -np.inf] = 0
        board = board / np.log2(maxVal)
        #print(board)

        return board

    # adds a random 2 or 4 to the board.
    def addRandomTile(self):
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
            return newVal

    # returns the score of the board, i.e., the sum of all the pieces on the board (not the official way to calculate score)
    def score(self):
        score = 0
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                score += val
        return score

    # returns the highest element of the board
    def highest(self):
        highest = 0
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val > highest:
                    highest = val
        return highest

    # make a left move. Used for each other implementation
    def left(self, print=True):
        changed = False
        # copy the board
        old_board = copy.deepcopy(self.board)
        for index, row in enumerate(self.board):
            self.board[index] = self.moveRowLeft(row)
        
        newVal = 0
        if (old_board != self.board): 
            newVal = self.addRandomTile()
        return newVal, old_board != self.board

    # mirror the board, make a left move, and mirro the board again. Seems complicated but is actually the simplest way to implement
    # [2, 0, 0, 4] -> [4, 0, 0, 2] -> [4, 2, 0, 0] -> [0, 0, 2, 4]
    def right(self, print=True):
        self.flipBoard()
        newVal, moved = self.left()
        self.flipBoard()
        return newVal, moved

    # rotate board counterclockwise, move left, and rotate board clockwise
    def up(self, print=True):
        self.rotateCCW()
        newVal, moved = self.left()
        self.rotateCW()
        return newVal, moved
    
    # rotate board clockwise, move left, and rotate board counterclockwise
    def down(self, print=True):
        self.rotateCW()
        newVal, moved = self.left()
        self.rotateCCW()
        return newVal, moved

    # parse an array and make the appropriate move. For AI purposes.
    # onehot = [up, down, left, right]
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
