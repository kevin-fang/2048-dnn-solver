from random import choice, randint

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

class Board:
    testingBoard = [[0, 2, 2, 2], 
                     [0, 0, 0, 0], 
                     [0, 4, 0, 2], 
                     [0, 0, 32, 4]]

    # initialize with 4x4 board with two 2's randomly placed
    def __init__(self, testing=False):
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
    
    def flipBoard(self):
        board = self.board
        for index, row in enumerate(board):
            board[index] = row[::-1]
    
    def rotateCW(self):
        self.board = [list(a) for a in zip(*self.board[::-1])]
    
    def rotateCCW(self):
        for i in range(3):
            self.rotateCW()

    # adds a random 2 or 4 to the board
    def addRandomTile(self):
        emptyVals = []
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val == 0:
                    emptyVals.append((x, y))
        if len(emptyVals) == 0:
            return False
        else:
            newCoords = choice(emptyVals)
            newVal = choice(possibleRandom)
            self.board[newCoords[0]][newCoords[1]] = newVal
            return True

    # make a left move. Used for each other implementation
    def left(self):
        for index, row in enumerate(self.board):
            self.board[index] = moveRowLeft(row)
        self.addRandomTile()

    # flip board, move left, and flip board again. Seems complicated but is actually the simplest way to implement
    # [2, 0, 0, 4] -> [4, 0, 0, 2] -> [4, 2, 0, 0] -> [0, 0, 2, 4]
    def right(self):
        self.flipBoard()
        self.left()
        self.flipBoard()

    # rotate rows counterclockwise, move left, and rotate rows clockwise
    def up(self):
        self.rotateCCW()
        self.left()
        self.rotateCW()
    
    # rotate rows clockwise, move left, and rotate rows counterclockwise
    def down(self):
        self.rotateCW()
        self.left()
        self.rotateCCW()

    # parse an array and make the appropriate move. For AI purposes.
    # [up, down, left, right]
    def oneHotMove(self, oneHotArray):
        if oneHotArray[0] == 1: 
            self.up()
        elif oneHotArray[1] == 1:
            self.down()
        elif oneHotArray[2] == 1:
            self.left()
        elif oneHotArray[3] == 1:
            self.right()