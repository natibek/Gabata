import copy


class Board:
    """
    Board class contain all attributes and methods dealing with the game player.
    Implementation of Gabata game rules
    """

    def __init__(self):
        """
        Constructor for instantiating a board with the start scores and the first player
        """
        self.score = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.sequence = [1]

    def get_player(self):
        return self.sequence[-1]

    def set_player(self, player):
        self.sequence.append(player)

    def get_sequence(self):
        return self.sequence

    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_score(self, score_list):
        self.score = score_list

    def get_score(self):
        return self.score

    def valid_moves(self, player: int):
        """
        Returns list of all the valid moves for a given player

        Input: player (int) -> player 1 or 2

        Output: valid_moves (list) -> list of valid moves
        """

        valid_move = []

        if player == 1:
            for i in range(6):
                if self.score[i] != 0:
                    valid_move.append(i)

        elif player == 2:
            for i in range(7, 13):
                if self.score[i] != 0:
                    valid_move.append(i)
        return valid_move

    def copy(self):
        """
        Returns a deep copy of the current board

        Output: new_copy (Board) -> copied board
        """

        new_copy = Board()
        new_copy.set_score(copy.deepcopy(self.get_score()))
        new_copy.set_sequence(copy.deepcopy(self.get_sequence()))

        return new_copy

    def points(self, player: int):
        """
        Returns the number of points a given player has scored

        Input: player (int) -> 1 or 2
        """
        if player == 1:
            return self.score[6]
        else:
            return self.score[13]

    def empty(self, player: int):
        """
        Checks if the player has no marbles left on their side

        Input: player (int) -> 1 or 2

        Output: True or False
        """

        if player == 1:
            if sum(self.score[0:6]) == 0:
                return True
        else:
            if sum(self.score[7:13]) == 0:
                return True

        return False

    def move(self, pos: int):
        """
        Function makes move on the board and changes are made to the state of the board

        Inputs:
            pos (int): position the player wants to start moving from
        """
        moves = []

        change = {key: value for key, value in zip(range(0, 13), range(12, -1, -1))}
        seq_switch = {1: 2, 2: 1}
        player = self.get_player()

        if pos in self.valid_moves(player):
            while player == self.sequence[-1]:
                hand = self.score[pos]  # number of marbles in the chosen position
                self.score[pos] = 0

                moves.append((pos, "Start"))

                for _ in range(hand):
                    pos += 1
                    if (pos == 6 and player == 2) or (
                        pos == 13 and player == 1
                    ):  # checks if position is in the opponent deposit slots
                        pos += 1
                    if pos == 14:  # checks if the position is at the end of the list
                        pos = 0
                    self.score[pos] += 1
                    moves.append((pos, "Play"))

                if (pos == 6 and player == 1) or (
                    pos == 13 and player == 2
                ):  # checks if last move is to player's own deposit slot
                    self.sequence.append(player)
                    self.end_turn(moves)
                    break
                elif (pos == 6 and player == 2) or (
                    pos == 13 and player == 1
                ):  # checks if last move is into opponent's deposit slot
                    self.set_player(seq_switch[player])
                    self.end_turn(moves)
                    break
                elif self.score[pos] == 1:  # last move into empty slot
                    if (0 <= pos < 6 and player == 1) or (
                        7 <= pos < 13 and player == 2
                    ):  # case where last move to player's own side into empty slot
                        if (
                            self.score[change[pos]] != 0
                        ):  # check if symmetric side is not empty
                            self.score[pos] = 0
                            pos = change[pos]  # continue moving from symmetric side
                            self.score[pos] += 1
                        else:  # symmetric slot is empty
                            self.set_player(seq_switch[player])
                            self.end_turn(moves)
                            break
                    else:
                        self.set_player(
                            seq_switch[player]
                        )  # into opponent's empty slot
                        self.end_turn(moves)
                        break

    def end_turn(self, moves):
        if self.empty(2):  # if player has no legal moves left switch players
            self.set_player(1)

        if self.empty(1):
            self.set_player(2)
        return moves

    def get_winner(self):
        """
        Returns the outcome/winner of the game
        """
        if self.points(1) > self.points(2):
            return 1
        elif self.points(2) > self.points(1):
            return 2
        return 0

    def game_over(self):
        """
        Returns wether game is over or not
        """
        if self.empty(1) and self.empty(2):
            return True
        return False
