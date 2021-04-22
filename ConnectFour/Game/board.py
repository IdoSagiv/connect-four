import copy

EMPTY_CELL = 0


class Board:
    """
    class that defines board objects.
    """

    def __init__(self, row, col):
        """
        constructor of board object.
        :param row: amount of rows
        :param col: amount of columns
        """
        self.__board = self.__create_board(row, col)

        # Key = col num, Value = number of disks in the col.
        self.__col_dict = dict((i, 0) for i in range(col))

    # public methods
    def make_move(self, row, col, name):
        """
        method of board that makes moves in the board.
        :param row: row coordinate
        :param col: col coordinate
        :param name: of player that made the move
        :return: True if could make the move, False if not
        """
        if self.__is_valid_move(row, col):
            self.__board[row][col] = name
            self.__col_dict[col] += 1
            return True
        return False

    def get_cell_content(self, row, col):
        """
        method that returns the content of given cell. if the cell is not in
        the board, raises exception.
        :param row: coordinate
        :param col: coordinate
        :return: content of the cell - None if empty or the number of the
        player.
        """
        if not self.__cell_in_board(row, col):
            raise ValueError("Illegal location.")
        elif self.__board[row][col] != EMPTY_CELL:
            return self.__board[row][col]

    def get_col_dict(self):
        return copy.deepcopy(self.__col_dict)

    # private methods
    def __create_board(self, row, col):
        """
        method that creates board in size row X cols.
        :return: board matrix
        """
        new_board = []
        for i in range(row):
            line = []
            for j in range(col):
                line.append(EMPTY_CELL)
            new_board.append(line)
        return new_board

    def __cell_in_board(self, row, col):
        """
        checks if a given cell is in the board.
        :return: bool value
        """
        return 0 <= row < len(self.__board) and 0 <= col < len(self.__board[0])

    def __is_valid_move(self, row, col):
        """
        checks if a given move is valid.
        :return: bool value
        """
        return self.__cell_in_board and self.__board[row][col] == EMPTY_CELL
