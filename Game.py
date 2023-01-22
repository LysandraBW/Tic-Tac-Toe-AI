import random
import time

from AI import smart_move
from Board import Board
from Player import Player
from random import randint


board = Board()
players = [Player("X", 0), Player("O", 1)]


# Configures who/what is playing against who/what
def configure_players():
    answer_player = input("\nEnter C to Continue as Before.\nEnter R to Play with Robot.\nEnter H to Play with Human.\nEnter N to Watch Robots Compete.\n\nEnter Here: ").strip().upper()

    # User is changing configuration of previous game
    if answer_player != "C":

        # Reset stored statistics
        board.reset_ties()
        players[0].reset_wins()
        players[1].reset_wins()

        # Human user is playing against robot
        if answer_player == "R":
            players[0].make_human("H")
            players[1].make_robot("R")

        # Human user is playing against human
        if answer_player == "H":
            players[0].make_human("X")
            players[1].make_human("O")

        # Robot is playing against robot
        if answer_player == "N":
            players[0].make_robot("X")
            players[1].make_robot("O")


# Configures who/what goes first
def configure_dibs():
    answer_dibs = input("\nEnter R for Toss-Up.\nEnter 0 for Player 0's Dibs.\nEnter 1 for Player 1's Dibs.\n\nEnter Here: ").strip().upper()

    # Player 0 goes first
    if answer_dibs == "0":
        return 0

    # Player 1 goes first
    if answer_dibs == "1":
        return 1

    # A random number determines dibs
    return randint(0, 1) != 1


# Gets human player's next move
def get_human_move(turn):
    while True:
        # Get space index from input
        space_index = int(input(players[turn].get_symbol() + " Turn, Enter Space: "))

        # A valid space index will break out of the function (the function called returned True)
        # An invalid space index will be prompted for correction (the function called returned False)
        if board.add_player_move(players[turn], space_index):
            break


# Gets robot player's next move
def get_robot_move(turn):
    # To avoid the same outcomes, I have the robot initially choose a random space
    if board.available_spaces() == 9:
        space_index = randint(0, 8)
    # Use smart_move function to get best space
    else:
        space_index = smart_move(board, players[player_turn], players[1 if turn == 0 else 0])

    # I am assuming the space_index is valid as this is a robot
    board.add_player_move(players[player_turn], space_index)


# Making the robot seem a less robotic
def simulate_robot_move(turn):
    # Announcing the robot's turn as if it was a human
    print(players[turn].get_symbol() + " Turn")

    # The robot will seem to deeply ponder on their choice
    time.sleep(random.uniform(0.2, 5.0))


# Printing the results of the game
def print_results():
    # Tie
    if board.get_tie():
        print("TIE\nGAME OVER!")

    # Win
    else:
        print("PLAYER " + players[board.get_winner()].get_symbol() + " WON.\nGAME OVER!")


# Printing the statistics of the players
def print_statistics():
    print("\nPlayer " + players[0].get_symbol() + " Wins: " + str(players[0].get_wins()))
    print("Player " + players[1].get_symbol() + " Wins: " + str(players[1].get_wins()))
    print("Ties: " + str(board.get_ties()))


# To play again, the board must be cleared of moves, and the players' turns must be cleared
def clean_up():
    board.reset()
    players[0].reset_moves()
    players[1].reset_moves()


# If a True is returned, the game is to be exited. If False returned, continue playing
def exit_game():
    answer = input("\nEnter C to Continue.\nEnter E to Exit.\n\nEnter Here: ").strip().upper()
    return answer == "E"


# Kind of clears up the terminal, at least on my end
def clear_terminal():
    print("\n" * 50)


while True:

    # Configuring game
    configure_players()
    player_turn = configure_dibs()

    clear_terminal()

    print("\nGAME\nTIC-TAC-TOE\n")

    # Print board
    board.draw()

    while True:
        # If the current turn is played by a human
        if players[player_turn].human():
            get_human_move(player_turn)

        # If the current turn is played by a robot
        else:
            get_robot_move(player_turn)
            simulate_robot_move(player_turn)

        # Print board
        board.draw()

        # Check for outcomes
        if board.update(*players):
            break

        # Switching turns
        player_turn = 0 if player_turn == 1 else 1

    # Print data
    print_results()
    print_statistics()

    # Clear board, clear players' turns
    clean_up()

    if exit_game():
        break

print("\nThanks For Playing! Have a Good Day. :-D\nLBW")
