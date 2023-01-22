# Lists of moves that win the game
WIN_ARR = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


# Checks if the given moves contains one of the winning moves
def has_winning_move(moves):
    moves_ = set(moves)

    for winning_arrangement in WIN_ARR:
        # If a list/set of winning moves is found in the given moves, there is a win
        if set(winning_arrangement).issubset(moves_):
            return True

    # No winning moves were found
    return False


class Player:

    def __init__(self, symbol, index):
        # Used to represent moves on the board
        self.symbol = symbol

        # Used for updating game state
        self.index = index

        # Contains player's moves (the indexes of the spaces)
        self.moves = []

        # Is this player a robot?
        self.robot = False

        # This player's number of wins
        self.wins = 0

    # Add a move to player's list of moves
    def add_move(self, space_index):
        self.moves.append(space_index)

    # Manually sets the player's move, used for testing
    def set_moves(self, moves):
        self.moves = moves

    # Returns True if player has a winning arrangement; Returns False if not
    def won(self):
        return has_winning_move(self.moves)

    # Adds a win for statistics
    def add_win(self):
        self.wins += 1

    # Erases stored wins, used when changing players
    def reset_wins(self):
        self.wins = 0

    # Erases stored moves, used when starting new game
    def reset_moves(self):
        self.moves = []

    # It's a human if it is not a robot
    def human(self):
        return not self.robot

    # Ditto
    def make_robot(self, symbol=None):
        self.robot = True
        if symbol is not None:
            self.symbol = symbol

    # Ditto
    def make_human(self, symbol=None):
        self.robot = False
        if symbol is not None:
            self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def get_index(self):
        return self.index

    def get_moves(self):
        return self.moves

    def get_wins(self):
        return self.wins


