"""
LBS (Last Block Standing)
Created by Jack Phillips
This program allows users to play or analyze positions of Last Block Standing, a combinatorial game of my own creation.
"""
import timeit

class LBS:
    def __init__(self, x, y, board):
        """
        __init__ initializes the game of LBS based
        :param x: the width of the game board
        :param y: the height of the game board
        :param board: a 2d array representing the game board
        preconditions:
            the inputs are for a valid game board
        """
        self.x = x
        self.y = y
        self.board = board
        self.left_children = set()
        self.right_children = set()
        self.outcome_class = None

    def drop_blocks(self):
        """
        drop_blocks removes any blocks that are not a part of a complete row or complete column
        """
        updated = True
        while updated:
            updated = False
            for row in range(self.y):
                for col in range(self.x):
                    if self.board[row][col] != '-' and (not self.is_full_row(row)) and (not self.is_full_col(col)):
                        self.board[row][col] = '-'
                        updated = True

    def is_full_row(self, row):
        """
        if_full_row returns whether a row is completely full
        :param row: the row in question
        :return: whether the row is full
        """
        for col in range(self.x):
            if self.board[row][col] == '-':
                return False
        return True

    def is_full_col(self, col):
        """
        if_full_col returns whether a column is completely full
        :param col: the column in question
        :return: whether the column is full
        """
        for row in range(self.y):
            if self.board[row][col] == '-':
                return False
        return True

    def create_tree(self):
        """
        create_tree recursively populates the children of every game position, but stop making children when it has a
        winning position for both players.
        """
        left_blocks = ['B', 'G']
        right_blocks = ['R', 'G']
        for row in range(self.y):
            for col in range(self.x):
                if self.board[row][col] in left_blocks and not self.left_can_win():
                    new_board = [row[:] for row in self.board]
                    child = LBS(self.x, self.y, new_board)
                    child.board[row][col] = '-'
                    child.drop_blocks()
                    child.create_tree()
                    child.define_outcome_class()
                    self.left_children.add(child)
                if self.board[row][col] in right_blocks and not self.right_can_win():
                    new_board = [row[:] for row in self.board]
                    child = LBS(self.x, self.y, new_board)
                    child.board[row][col] = '-'
                    child.drop_blocks()
                    child.create_tree()
                    child.define_outcome_class()
                    self.right_children.add(child)
                if self.left_can_win() and self.right_can_win():
                    return

    def left_can_win(self):
        """
        left_can_win returns whether the left player can win the game if they go next
        :return: whether the left player can win going next
        """
        for child in self.left_children:
            if child.outcome_class in ['L', 'P']:
                return True
        return False

    def right_can_win(self):
        """
        right_can_win returns whether the right player can win the game if they go next
        :return: whether the right player can win going next
        """
        for child in self.right_children:
            if child.outcome_class in ['R', 'P']:
                return True
        return False

    def left_can_move(self):
        """
        left_can_move returns whether the left player has any more legal moves in the current game
        :return: whether the left player has any more legal moves
        """
        for row in range(self.y):
            for col in range(self.x):
                if self.board[row][col] in ['B', 'G']:
                    return True
        return False

    def right_can_move(self):
        """
        right_can_move returns whether the right player has any more legal moves in the current game
        :return: whether the right player has any more legal moves
        """
        for row in range(self.y):
            for col in range(self.x):
                if self.board[row][col] in ['R', 'G']:
                    return True
        return False

    def find_winning_move(self, isLeft):
        """
        find_winning_move finds a winning move based on whose turn it is and the current board position
        :param isLeft: whether it is the left player's turn
        :return: the winning board position
        """
        if isLeft:
            for child in self.left_children:
                if child.outcome_class in ['L', 'P']:
                    return child.board
        else:
            for child in self.right_children:
                if child.outcome_class in ['R', 'P']:
                    return child.board

    def find_legal_move(self, isLeft):
        """
        find_legal_move finds a legal move based  on whose turn it is and the current board position
        :param isLeft: whether it is the left player's turn
        :return: the legal board position
        """
        if isLeft:
            for child in self.left_children:
                return child.board
        else:
            for child in self.right_children:
                return child.board

    def define_outcome_class(self):
        """
        define_outcome_class defines the outcome class of a game as either L (positive), R (negative), N (fuzzy), or
        P (zero)
        :return: the outcome class
        """
        left_can_win = self.left_can_win()
        right_can_win = self.right_can_win()
        if left_can_win and right_can_win:
            self.outcome_class = 'N'
        elif left_can_win:
            self.outcome_class = 'L'
        elif right_can_win:
            self.outcome_class = 'R'
        else:
            self.outcome_class = 'P'

    def display_LBS(self):
        """
        display_LBS prints the board out
        """
        for row in range(self.y):
            for col in range(self.x):
                print(self.board[row][col], end='')
            print()

def main():
    """
    main allow the user to select whether they would like to play a game or analyze a game
    """
    while True:
        response = input("Please select 'play', 'analyze', or 'quit': ")
        if response == 'play':
            gameType = input("Please select whether you would like to play against the 'computer' or an 'opponent': ")
            if gameType == 'opponent':
                filename = input('Input the name of the file containing the LBS board: ')
                with open(filename) as file:
                    rows = 0
                    board = []
                    for line in file:
                        rows += 1
                        cols = 0
                        row = []
                        for ch in line:
                            cols += 1
                            if ch in ['B', 'R', 'G', '-']:
                                row.append(ch)
                        board.append(row)
                game = LBS(cols, rows, board)
                while True:
                    if not game.left_can_move():
                        game.display_LBS()
                        print('Game over, second player won')
                        break
                    print('First players turn:')
                    game.display_LBS()
                    while True:
                        row_choice = int(input('Enter row number: ')) - 1
                        col_choice = int(input('Enter col number: ')) - 1
                        print()
                        if row_choice > rows or col_choice > cols or game.board[row_choice][col_choice] in ['-', 'R']:
                            print('Invalid move, try again')
                        else:
                            game.board[row_choice][col_choice] = '-'
                            game.drop_blocks()
                            break
                    if not game.right_can_move():
                        game.display_LBS()
                        print('Game over, first player won')
                        break
                    print('Second players turn:')
                    game.display_LBS()
                    while True:
                        row_choice = int(input('Enter row number: ')) - 1
                        col_choice = int(input('Enter col number: ')) - 1
                        print()
                        if row_choice > rows or col_choice > cols or game.board[row_choice][col_choice] in ['-', 'B']:
                            print('Invalid move, try again')
                        else:
                            game.board[row_choice][col_choice] = '-'
                            game.drop_blocks()
                            break
            elif gameType == 'computer':
                filename = input('Input the name of the file containing the LBS board: ')
                with open(filename) as file:
                    rows = 0
                    board = []
                    for line in file:
                        rows += 1
                        cols = 0
                        row = []
                        for ch in line:
                            cols += 1
                            if ch in ['B', 'R', 'G', '-']:
                                row.append(ch)
                        board.append(row)
                game = LBS(cols, rows, board)
                print("Would you like to play 'first' or 'second': ")
                while True:
                    response = input('> ')
                    if response == 'first':
                        isFirst = True
                        break
                    elif response == 'second':
                        isFirst = False
                        break
                    else:
                        print("Response not recognized")
                while True:
                    if not game.left_can_move():
                        game.display_LBS()
                        if isFirst:
                            print('Game over, computer won')
                        else:
                            print('Game over, you won')
                        break
                    if isFirst:
                        print('First players turn:')
                        game.display_LBS()
                        while True:
                            row_choice = int(input('Enter row number: ')) - 1
                            col_choice = int(input('Enter col number: ')) - 1
                            print()
                            if row_choice > rows or col_choice > cols or game.board[row_choice][col_choice] in ['-', 'R']:
                                print('Invalid move, try again')
                            else:
                                game.board[row_choice][col_choice] = '-'
                                game.drop_blocks()
                                break
                    else:
                        print("Computer's turn:")
                        game.display_LBS()
                        print()
                        board_copy = [row[:] for row in game.board]
                        game_copy = LBS(game.x, game.y, board_copy)
                        game_copy.create_tree()
                        game_copy.define_outcome_class()
                        if game.outcome_class in ['N', 'L']:
                            game.board = game_copy.find_winning_move(True)
                        else:
                            game.board = game_copy.find_legal_move(True)
                    if not game.right_can_move():
                        game.display_LBS()
                        if isFirst:
                            print('Game over, you won')
                        else:
                            print('Game over, computer won')
                        break
                    if not isFirst:
                        print('Second players turn:')
                        game.display_LBS()
                        while True:
                            row_choice = int(input('Enter row number: ')) - 1
                            col_choice = int(input('Enter col number: ')) - 1
                            print()
                            if row_choice > rows or col_choice > cols or game.board[row_choice][col_choice] in ['-', 'B']:
                                print('Invalid move, try again')
                            else:
                                game.board[row_choice][col_choice] = '-'
                                game.drop_blocks()
                                break
                    else:
                        print("Computer's turn:")
                        game.display_LBS()
                        print()
                        board_copy = [row[:] for row in game.board]
                        game_copy = LBS(game.x, game.y, board_copy)
                        game_copy.create_tree()
                        game_copy.define_outcome_class()
                        if game.outcome_class in ['N', 'R']:
                            game.board = game_copy.find_winning_move(False)
                        else:
                            game.board = game_copy.find_legal_move(False)
            else:
                print('Response not recognized')
                return
        elif response == 'analyze':
            filename = input('Input the name of the file containing the LBS board: ')
            with open(filename) as file:
                rows = 0
                board = []
                for line in file:
                    rows += 1
                    cols = 0
                    row = []
                    for ch in line:
                        cols += 1
                        if ch in ['B', 'R', 'G', '-']:
                            row.append(ch)
                    board.append(row)
            start = timeit.default_timer()
            game = LBS(cols, rows, board)
            game.create_tree()
            game.define_outcome_class()
            stop = timeit.default_timer()
            game.display_LBS()
            print()
            print('Outcome class:', game.outcome_class)
            print('Analysis time:', stop - start)
        elif response == 'quit':
            return
        else:
            print('Response not recognized, try again:')

if __name__ == '__main__':
    main()