from Player import Player, has_winning_move


class TheoreticalPlayer(Player):
    def __init__(self, player):
        # We must never forget who we came from
        super().__init__(player.get_symbol(), player.get_index())

        # Copying down the moves we have already made, I call this "concrete"
        self.moves = player.get_moves().copy()

        # Think of the theoretical moves as an extension of the "concrete" moves
        self.theoretical_moves = []

    # Verbatim
    def add_theoretical_move(self, space_index):
        self.theoretical_moves.append(space_index)

    # Removes the last move and returns the space index so the TheoreticalBoard object
    # can remove it from its theoretical board as well
    def pop_theoretical_move(self):
        return self.theoretical_moves.pop()

    # If the player's theoretical moves have allowed it to win, return True; Else we return False
    def theoretically_won(self):
        return has_winning_move(self.agg_moves())

    # Combines theoretical and concrete (the moves that have actually been made) moves together
    def agg_moves(self):
        return self.moves + self.theoretical_moves