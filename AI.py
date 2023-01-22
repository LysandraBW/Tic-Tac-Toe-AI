import math

from T_Board import TheoreticalBoard
from T_Player import TheoreticalPlayer
from Board import ROWS, COLS, two_to_one, space_taken


MAX_TURN = 0
MIN_TURN = 1


def smart_move(board, maximizing, minimizing):
    t_board = TheoreticalBoard(board)
    t_maximizing = TheoreticalPlayer(maximizing)
    t_minimizing = TheoreticalPlayer(minimizing)

    return minmax(t_board, t_maximizing, t_minimizing, MAX_TURN, 1, True)[0]


def minmax(t_board, t_maximizing, t_minimizing, turn, depth, start=False):
    return_value = math.inf

    # If the maximizing player wins, return (1.0/depth)
    if t_maximizing.theoretically_won():
        return_value = 1.0 / depth

    # If the minimizing player wins, return (-1.0/depth)
    elif t_minimizing.theoretically_won():
        return_value = -1.0 / depth

    # If there is a tie, return 0.0
    elif t_board.full_house():
        return_value = 0.0

    # There are 19,683 ways to fill the board. If I let this function attempt that, the program would
    # terminate. So I'm limiting the search depth to anything less than 10.
    # This can probably be changed for experimentation?
    elif depth > 10:
        return_value = 0.0

    # If an outcome has been reached, return that outcome
    if return_value != math.inf:
        return return_value

    # The maximizing player is trying to get the highest score possible
    # The minimizing player is trying to get the lowest score possible
    top_score = math.inf if turn == MIN_TURN else -math.inf

    # The move associated with the top score is returned when
    # the smart argument is equal to True (when we have found the best outcome)
    top_move = -1

    # If an outcome has not been reached, we will find the best outcome out of all the outcomes
    # by iterating through the board and testing out the various possibilities
    for row in range(ROWS):
        for col in range(COLS):

            # Any taken spaces are a no-go, we can't use those
            if space_taken(t_board.get_theoretical_board(), row, col):
                continue

            space_index = two_to_one(row, col)

            # Can the two if statements be simplified into something more
            # sleek? Perhaps! But it's easier for me to understand when it's
            # drawn out, so I will not be changing it

            # If it is the maximizing player's turn (we favor them)
            if turn == MAX_TURN:

                # Add the move we found
                t_board.add_theoretical_player_move(t_maximizing, space_index)

                # Get the score of this move
                score = minmax(t_board, t_maximizing, t_minimizing, MIN_TURN, depth + 1)

                # If this score is greater than our top score, we have some replacing to do (more is better)
                if score > top_score:
                    top_score = score
                    top_move = space_index

                # We can pop off the added turn as we no longer need it.
                # We also need to test other theoretical moves, meaning if we didn't pop/remove this
                # recently added theoretical move, we would run into issues
                t_board.pop_theoretical_move(t_maximizing.pop_theoretical_move())

            # If it is the minimizing player's turn (we do not favor them)
            if turn == MIN_TURN:

                # Add the move we found
                t_board.add_theoretical_player_move(t_minimizing, space_index)

                # Get the score of this move
                score = minmax(t_board, t_maximizing, t_minimizing, MAX_TURN, depth + 1)

                # If this score is less than our top score, we have some replacing to do (less is better)
                if score < top_score:
                    top_score = score
                    top_move = space_index

                # I explained this a few lines up
                t_board.pop_theoretical_move(t_minimizing.pop_theoretical_move())

    # The score is not needed when we are finally done, but it's there for testing purposes
    # But when we are finally done, we can just return the optimal move
    if start:
        return top_move, top_score

    # Return the top score of this player's turn:
    # The maximizing player will return the highest score
    # The minimizing player will return the lowest score
    return top_score
