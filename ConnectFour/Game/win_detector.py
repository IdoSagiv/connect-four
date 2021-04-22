WIN_SEQUENCE = 4
DIRECTIONS_PROG = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
                   "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}


class WinDetector:
    """
    a class responsible on detect a win in a given board.
    """

    def __init__(self, board):
        """
        :param board: the board object that the class will look in.
        """
        self.__board = board
        self.__win_seq = []
        # Defines the funcs that search for win in the different directions.
        self.__won_row = self.__win_searcher(["E", "W"])
        self.__won_col = self.__win_searcher(["S"])
        self.__won_diagonal_a = self.__win_searcher(["SE", "NW"])
        self.__won_diagonal_b = self.__win_searcher(["NE", "SW"])

    # Public methods:

    def is_won(self, last_move, player, board=None):
        """
        private method that checks if the given player has won with
        the given move.
        :var last_move: a tuple of ints indicates the last coordinate that was
            played (row,col).
        :return: bool value.
        """
        if board is None:
            board = self.__board
        return (self.__won_row(board, last_move, player) or
                self.__won_col(board, last_move, player) or
                self.__won_diagonal_a(board, last_move, player) or
                self.__won_diagonal_b(board, last_move, player))

    def get_win_seq(self):
        """ Getter """
        return self.__win_seq

    # Private methods:

    def __win_searcher(self, directions):
        """
        get directions and return a func that search for win in those
        directions.
        :param directions: A list of strings each one represent a direction
        :return: func.
        """

        def searcher(board, last_move, player):
            """
            get player and last move and checks i the player won with this
            move (in the cashed directions).
            :return: bool value.
            """
            # set win seq to the last move
            win_seq = [[last_move[0], last_move[1]]]
            is_won = False
            for direction in directions:
                if len(win_seq) < WIN_SEQUENCE:
                    temp_seq = self.__count_sequence(board, direction,
                                                     last_move, player)
                    win_seq += temp_seq
                else:
                    break

            if len(win_seq) >= WIN_SEQUENCE:
                is_won = True
                self.__win_seq = win_seq
            return is_won

        return searcher

    def __count_sequence(self, board, direction, start_point, player):
        """
        a method that counts the sequence of following disks of same
        player. this method can count the sequences in the given direction
        :param direction: wanted direction to count in.
        :var start_point: a tuple of ints indicates the point on the board we
            want to count the sequence from (row,col)
        :var player:
        :return: sequence
        """
        seq = []
        row, col = start_point[0], start_point[1]
        delta_x, delta_y = DIRECTIONS_PROG[direction]
        # progression on the axises
        col += delta_x
        row += delta_y
        # need to check maximum 3 cells
        for i in range(WIN_SEQUENCE - 1):
            try:
                if board.get_cell_content(row, col) != player:
                    break
            except ValueError:
                break

            seq.append([row, col])
            col += delta_x
            row += delta_y
        return seq
