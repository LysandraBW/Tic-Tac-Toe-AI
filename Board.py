from Color import *
import math


ROWS = 3
COLS = 3
SPACES = ROWS * COLS


# Converts the 1D index of a 2D container to its equivalent row and column
# Example: Lets say we took a 3x3 array and turned it into a 1x9 array. The element at
# index 4 of the 1x9 array is the same element at row 2 column 2 of the 3x3 array.
def one_to_two(i):
    r = math.floor(i / COLS)
    c = i - r * COLS
    return r, c


# Converts an element's row and column in a 2D container to its equivalent 1D index
# Example: Lets say we took a 1x9 array and turned it into a 3x3 array. The element at
# row 2 column 2 of the 3x3 array is the same element at index 4 of the 1x9 array.
def two_to_one(r, c):
    return r * COLS + c


# Draws the board; the color parameter changes which colors are used; COLORS is a dictionary defined in Color.py
def draw_board(board, color=COLORS):

    print("\nBoard")

    for row in range(ROWS):
        for col in range(COLS):

            space_index = two_to_one(row, col)
            space_token = board[row][col]

            # If the current space is taken, we print the token
            if space_token is None:
                print(str(space_index), end="")

            # If the current space is empty, we print its space index
            else:
                print(color[space_token] + space_token, end=color["END"])

            # Foresight
            next_space = space_index + 1

            # We have reached the last space and are now done printing
            if next_space >= SPACES:
                print("\n")
                return

            # We are at the end of a row and must print a horizontal divider
            if (space_index + 1) % 3 == 0:
                print("\n---------")

            # We separate adjacent spaces via a vertical divider
            else:
                print(" | ", end="")


# Returns True if the element at the specified row and col of the given board is taken.
# Returns False if it's empty (None)
def space_taken(board, row, col):
    return not board[row][col] is None


# Returns True if the given space index is invalid
# Returns False if the given space is valid (012345678)
def bad_space(space_index):
    return space_index < 0 or space_index > 8


class Board:

    def __init__(self):
        # Initializing an empty 3x3 list
        self.board = [[None] * COLS for _ in range(ROWS)]

        # The number of total moves made by the players
        self.moves = 0

        # An integer representing the index of the winner if there is a winner
        # False if no winner
        self.winner = False

        # True if there is a tie; False if there is not
        self.tie = False

        # The number of ties this board has witnessed
        self.ties = 0

    # Draw the board
    def draw(self):
        draw_board(self.board)

    # Adds a player's move to the board, validity of move is also checked
    def add_player_move(self, player, space_index):
        # If nonexistent space, we do not add the move
        if bad_space(space_index):
            return False

        row, col = one_to_two(space_index)

        # If the space is taken, we do not add the move
        if space_taken(self.board, row, col):
            return False

        # Add move via player's symbol to board
        self.board[row][col] = player.get_symbol()

        # Add move to player's moves
        player.add_move(space_index)

        # A move has been made, so we increment the number of moves
        # Did I really need to comment this?
        self.moves += 1

        return True

    def update(self, player0, player1):
        # If player 0 won
        if player0.won():
            self.winner = player0.get_index()
            player0.add_win()
            return True

        # If player 1 won
        if player1.won():
            self.winner = player1.get_index()
            player1.add_win()
            return True

        # If no player has won and there are no more spaces, there is a tie!
        if self.moves >= SPACES:
            self.tie = True
            self.add_tie()
            return True

        return False

    # It doesn't get as literal as this
    def add_tie(self):
        self.ties += 1

    # Resets the board so it can be played again
    def reset(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.moves = 0
        self.winner = False
        self.tie = False

    # Resets the number of ties to 0; used when changing players
    def reset_ties(self):
        self.ties = 0

    # The number of available spaces
    def available_spaces(self):
        return SPACES - self.moves

    def get_tie(self):
        return self.tie

    def get_winner(self):
        return self.winner

    def get_moves(self):
        return self.moves

    def get_board(self):
        return self.board

    def get_ties(self):
        return self.ties