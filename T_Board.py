from Board import Board, SPACES, draw_board, bad_space, space_taken, one_to_two
from Color import COLORS_ALT


class TheoreticalBoard(Board):

    def __init__(self, board):
        super().__init__()

        # We must catch up our theoretical board by basically copying the board
        self.board = board.get_board().copy()
        self.moves = board.get_moves()
        self.winner = board.get_winner()
        self.tie = board.get_tie()

        # I am not sure why, but any changes to theoretical_board will change the board variable (line 11)
        # This board is used when testing the possible moves to be made
        self.theoretical_board = board.get_board().copy()
        self.theoretical_moves = 0

        # I know theoretical is a long word, but I thought it was kind of funny

    # Draws the board, but uses different colors for testing purposes
    def draw(self):
        draw_board(self.theoretical_board, COLORS_ALT)

    # Adds a fake move so that we can find the best move
    def add_theoretical_player_move(self, theoretical_player, space_index):
        # Don't add if the space doesn't exist
        if bad_space(space_index):
            return False

        row, col = one_to_two(space_index)

        # Don't add if the space is already taken
        # Although I am not sure if I need this error-checking parts as robots
        # use this function
        if space_taken(self.theoretical_board, row, col):
            return

        # Add theoretical (emphasis on theoretical) to the theoretical board
        self.theoretical_board[row][col] = theoretical_player.get_symbol()

        # Also add the theoretical (theoretical) move to the theoretical (in theory) player
        theoretical_player.add_theoretical_move(space_index)

        # Now, this is just a theory, but the number of theoretical moves will
        # theoretically increase by 1 as we have added a theoretical move (your welcome)
        self.theoretical_moves += 1

        return True

    # To properly test all the possible moves, we need to undo the theoretical moves made after we have reached
    # an outcome. This function removes the given space index and consequently decrements the number of
    # theoretical moves
    def pop_theoretical_move(self, space_index):
        row, col = one_to_two(space_index)
        self.theoretical_board[row][col] = None
        self.theoretical_moves -= 1

    # I think this is a term used when playing cards. But to me, a full house is when there are no more
    # possible moves
    def full_house(self):
        return self.theoretical_moves + self.moves >= SPACES

    # Theoretically we would obtain the theoretical board, but this only limited to theory
    # as this is not a natural event
    def get_theoretical_board(self):
        return self.theoretical_board
