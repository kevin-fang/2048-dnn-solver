from random import randint


zero = lambda x: True if x == 0 else False

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

testing_board = [[2, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

class Board:

    def __init__(self, testing=False):
        self.board = [[0]*4 for i in range(4)]
        # game starts with two 2's placed randomly on the board
        x1, y1 = randint(0, 3), randint(0, 3)
        x2, y2 = randint(0, 3), randint(0, 3)
        
        # change y position if both values are the same
        while x1 == x2 and y1 == y2:
            y1 = randint(0, 3)

        self.board[x1][y1] = 2
        self.board[x2][y2] = 2
        if (testing):
            self.board = testing_board
    
    def left(self):
        for index, row in enumerate(self.board):
            self.board[index] = moveRowLeft(row)