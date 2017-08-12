from random import randint


def zero(item):
    if item == 0:
        return True
    else:
        return False

testing_board = [[0, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

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
        # start from the top row, and move everything left, adding if necessary
        # continue for other rows
        # [0, 0, 2, 0] -> [2, 0, 0, 0]
        # [2, 2, 2, 2] -> [4, 4, 0, 0]
        # loop through array until first nonzero item. If none exist, ignore.
        # if the very first item is zero, move the first nonzero item to the first position.
        # if the very first item is not zero, check if the first nonzero item has the same value. If it does, merge the values. Else, move it to the 2nd position.
        # repeat this for the second item.
        for row in self.board:
            '''
            for index, item in enumerate(row):
                if not zero(item):
                    checking_index = index + 1
                    for inner_index, value in enumerate(row[checking_index:]):
                        if not zero(value):
                            if value == row[index]:
                                row[index] *= 2
                                row[inner_index + checking_index] = 0
                            for 
                else:
                    for inner_index, value in enumerate(row[index + 1:]):
                        if not zero(value):
                            row[index] = value
                            row[inner_index + index] = 0
                
                print(row, index)
            '''
            for index, item in enumerate(row):
                # [2, 2, 2, 2] -> [4, 0, 4, 0]
                # [2, 0, 2, 0] -> [2, 0, 2, 0]
                # [0, 2, 2, 2] -> [0, 4, 0, 2]
                if index < len(row) - 1 and item == row[index + 1]:
                    row[index] *= 2
                    row[index + 1] = 0

 
    def right(self):
        pass
    
    def up(self):
        pass

    def down(self):
        pass

    def move1hot(self):
        pass