from .board import Board
from .win_detector import WinDetector

COL_SIZE = 7
ROW_SIZE = 6
TIE_RESULT = 0
WIN_SEQUENCE = 4
PLAYER_A = 1
PLAYER_B = 2


class Game:
    """
    class that defines game objects. these objects are responsible to run the
    'background' of the game.
    """

    def __init__(self):
        """
        constructor of this class.
        """
        self.__board = Board(ROW_SIZE, COL_SIZE)
        self.__player_a = PLAYER_A
        self.__player_b = PLAYER_B
        self.__round_counter = 1
        self.__win_detector = WinDetector(self.__board)
        # initial values
        self.__last_move = (PLAYER_A, -1, -1)
        self.__win_seq = []
        self.__game_over = False

    # public methods
    def make_move(self, column):
        """
        method that makes a move in the game with given column (adds one disk
        to this column).
        :param column: col of the move
        :return: True if could make the move. else - raises exception.
        """
        if (not self.__game_over) and self.__legal_move(column):
            row = (ROW_SIZE - 1) - self.__board.get_col_dict()[column]
            player_name = self.get_current_player()
            if self.__board.make_move(row, column, player_name):
                self.__round_counter += 1
                self.__last_move = (player_name, row, column)
                return True
        raise ValueError("Illegal move")

    def get_winner(self):
        """
        method that returns the winner of the game, if there is one.
        :return: if player won - it's number. if tie - 0. None if game is
        still on.
        """
        player = self.__last_move[0]
        last_coords = (self.__last_move[1], self.__last_move[2])
        if self.__win_detector.is_won(last_coords, player):
            self.__game_over = True
            return self.__last_move[0]  # The name of the winner

        if self.__is_tie():
            self.__game_over = True
            return TIE_RESULT

    def get_player_at(self, row, col):
        """
        method that returns the content of given cell.
        :param row: coordinate
        :param col: coordinate
        :return: cell content of the board
        """
        try:
            return self.__board.get_cell_content(row, col)
        except ValueError:
            return

    def get_current_player(self):
        """
        method that returns the player that it's his turn.
        :return: player number
        """
        if self.__round_counter % 2:
            return self.__player_a
        return self.__player_b

    def get_last_move(self):
        """
        method that returns the last move that has been made.
        :return: last move coordinates
        """
        row = self.__last_move[1]
        col = self.__last_move[2]
        return row, col

    def get_win_seq(self):
        """
        method that returns the winning disk's coordinates.
        :return: list of tuples (coordinates of winning cells). empty list
        if the winning sequence doesn't includes enough cells.
        """
        seq = self.__win_detector.get_win_seq()
        if len(seq) >= WIN_SEQUENCE:
            return seq[:4]
        return []

    def get_column_dict(self):
        return self.__board.get_col_dict()

    # private methods
    def __is_tie(self):
        """
        private method that checks if there is a tie.
        :return: bool value
        """
        for col, counter in self.__board.get_col_dict().items():
            if counter != ROW_SIZE:
                return False
        return True

    def __legal_move(self, col):
        """
        method that checks if a given move is a legal move.
        :param col: move
        :return: bool value
        """
        col_dict = self.__board.get_col_dict()
        return col in col_dict and col_dict[col] < ROW_SIZE
