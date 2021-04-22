from .board import Board
from .win_detector import WinDetector
import copy
import random

BOARD_ROW = 6
BOARD_COL = 7
EMPTY_CELL = 0
ITERATIONS = 2
PLAYER_A = 1
PLAYER_B = 2
SURE_WIN = 1000
SURE_LOSE = -100
POSS_WIN = 5
POSS_LOSE = -1
MIN_ITERATIONS = 1
TIMEOUT_LIMIT = 150


class AI:
    """
    class that defines AI object that calculates according to a given board and
    game turns.
    """

    def __init__(self, game, player):
        """
        constructor of the class. defines the fields of the objects.
        :param game: game object
        :param player: player number
        """
        self.__game = game
        self.__player = player
        if self.__player == PLAYER_A:
            self.__opponent = PLAYER_B
        else:
            self.__opponent = PLAYER_A

        self.__board = self.__build_board()
        self.__win_detect = WinDetector(self.__board)

        self.__possible_columns = []
        self.__moves_rating = {}
        self.__last_move = None

    # public methods
    def get_last_found_move(self):
        """
        method that returns the last found move of the game.
        :return: last move
        """
        return self.__last_move

    def find_legal_move(self, timeout=None):
        """
        method that is responsible for finding the AI's next move.
        :param timeout: time counter
        :return: move as column
        """
        if self.__game.get_winner() is not None:
            raise AttributeError("No possible AI moves.")

        iterations = ITERATIONS
        if timeout is not None and timeout < TIMEOUT_LIMIT:
            iterations = MIN_ITERATIONS

        self.__update_self_board()

        self.__init_moves_rating(self.__board)

        # rating the optional moves
        self.__update_moves_rating(self.__board, iterations)
        # choosing the best rates move
        self.__last_move = self.__choose_col()
        return self.__last_move

    def __build_board(self):
        """
        copies the game board.
        :return: board
        """
        board = Board(BOARD_ROW, BOARD_COL)

        for i in range(BOARD_ROW):
            for j in range(BOARD_COL):
                player = self.__game.get_player_at(i, j)
                if player:
                    board.make_move(i, j, player)
        return board

    def __update_self_board(self):
        """
        updates the board according to the 2 previous moves.
        :return: None
        """
        if self.__last_move is not None:
            self.__try_to_move(self.__board, self.__last_move, self.__player)
        for col in range(BOARD_COL):
            row = (BOARD_ROW - 1) - self.__board.get_col_dict()[col]
            player = self.__game.get_player_at(row, col)
            if player:
                self.__board.make_move(row, col, player)

    # private methods
    def __choose_col(self):
        """
        private method tht chooses the best rated possible move. after rating
        them in the dictionary.
        :return: column number (of this move)
        """
        col = max(self.__moves_rating, key=lambda i: self.__moves_rating[i])
        max_val = self.__moves_rating[col]

        options = [i for i in self.__moves_rating if
                   self.__moves_rating[i] == max_val]

        if len(options) > 1:
            col = random.choice(options)

        return col

    def __try_to_move(self, board, move, player):
        """
        method that tries to make a move on the bord.
        :param board: the board to play in.
        :param move: the col to play in.
        :param player:
        :return: If success-the played move, Else- False.
        """
        row = (BOARD_ROW - 1) - board.get_col_dict()[move]
        if board.make_move(row, move, player):
            return row, move
        return False

    def __update_moves_rating(self, board, rounds):
        """
        private method that is responsible for finding the best move. generates
        every possible move in the given number of next rounds and rates it
        accordingly.
        :param board: board object
        :param rounds: number of iterations
        :return: None
        """
        # base case: no more rounds
        if not rounds:
            return
        # make every possible move - of self
        my_moves = self.__get_poss_moves(board)
        for my_curr_move in my_moves:
            curr_board1 = copy.deepcopy(board)
            move_res1 = self.__try_to_move(curr_board1, my_curr_move,
                                           self.__player)
            if not move_res1:
                continue
            if self.__win_detect.is_won(move_res1, self.__player, curr_board1):
                if rounds == ITERATIONS:  # winning immediately - best opt
                    self.__moves_rating[my_curr_move] += SURE_WIN
                    break
                else:
                    self.__moves_rating[my_curr_move] += POSS_WIN
            else:
                opp_moves = self.__get_poss_moves(curr_board1)
                for opp_curr_move in opp_moves:
                    curr_board2 = copy.deepcopy(curr_board1)
                    move_res2 = self.__try_to_move(curr_board2, opp_curr_move,
                                                   self.__opponent)
                    if not move_res2:
                        continue
                    if self.__win_detect.is_won(move_res2, self.__opponent,
                                                curr_board2):
                        if rounds == ITERATIONS:
                            self.__moves_rating[my_curr_move] += SURE_LOSE
                        else:
                            self.__moves_rating[my_curr_move] += POSS_LOSE
                        break
                    else:
                        self.__last_move = max(self.__moves_rating,
                                               key=lambda i:
                                               self.__moves_rating[i])
                        # another turn - recursively
                        self.__update_moves_rating(curr_board2, rounds - 1)

    def __get_poss_moves(self, board):
        """
        private method that returns a list of possible moves in a given game.
        :param board: given game board
        :return:possible moves list
        """
        poss_moves = [j for j in range(BOARD_COL) if
                      board.get_col_dict()[j] < BOARD_ROW]

        return poss_moves

    def __init_moves_rating(self, board):
        """
        method that initializes moves rating dictionary.
        :return:None
        """
        self.__moves_rating = dict(
            (i, 0) for i in self.__get_poss_moves(board))
