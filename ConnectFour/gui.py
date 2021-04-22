import tkinter as tki
from tkinter import messagebox
from .Game.ai_player import AI
import time

CIRCLE_SIZE = 42
COLUMNS = 7
ROWS = 6
USER_TYPE = 1
AI_TYPE = 2
TIE = 0
AI_DELAY = 0.2
CELL_FRAME_IMG = "Resources/board_cell.png"
LOGO_PNG = 'Resources/logo.png'
SCORE_TXT = "PLAYER %s\n %d"
PLAYER_TURN_MSG = "Player %s turn"
WINNING_MSG = "Player %s WON!"
TIE_MSG = "Tie"
GAME_OVER = "Game Over"
PLAY_AGAIN_MSG = "Would you like to play again?"
WIN_CELLS_CLR = "gold3"
ERROR_MSG = "Invalid move"
ERROR_TITLE = "Error"
PLAYER_A_NAME = 'A'
PLAYER_B_NAME = 'B'


class Gui:
    """
    class that creates Gui objects. each Gui object can manage the graphical
    interface of current game.
    """

    def __init__(self, parent, game, player_a, player_b):
        # Fields
        self.__parent = parent
        self.__game = game
        self.__player_a = player_a
        self.__player_b = player_b
        if self.__player_a.get_type() == AI_TYPE:
            self.__ai_a = AI(game, self.__player_a.get_name())
        if self.__player_b.get_type() == AI_TYPE:
            self.__ai_b = AI(game, self.__player_b.get_name())
        self.__canvas_cells = []
        self.__another_game = False

        # GUI init
        self.__create_board(parent)
        labels_frame = tki.Frame(parent, bg="LightSkyBlue2")
        labels_frame.pack(fill=tki.Y, side=tki.RIGHT)
        self.__turn_info_lbl = tki.Label(labels_frame)
        self.__init_labels(labels_frame)

        # start game
        self.__parent.update()
        self.__turn_manager()

    # private methods
    def __ai_turn(self):
        """
        method that does one turn of the ai. gets a turn using the ai method
        and executes it on the gui.
        """
        player = self.__get_current_player()
        if player is self.__player_a:
            ai = self.__ai_a
        else:
            ai = self.__ai_b

        try:
            move = ai.find_legal_move()
            self.__make_move(player, move)
        except AttributeError:
            return

    def __turn_manager(self):
        """
        method that is being called consistently and calls ai turn if
        it needs to make a turn.
        """
        if self.__get_current_player().get_type() == AI_TYPE:
            self.__ai_turn()

    def __convert_name_to_player(self, player_name):
        """
        method that converts name (int) of player to the player's object.
        :param player_name: name (int)
        :return: player object.
        """
        if player_name == self.__player_a.get_name():
            return self.__player_a
        return self.__player_b

    def __get_current_player(self):
        """
        method that returns the current player (the player that it is his turn)
        :return: name of this player
        """
        player_name = self.__game.get_current_player()
        return self.__convert_name_to_player(player_name)

    def __finish_game(self):
        """
        method that is responsible to finish the game properly. including
        making the changes in the gui (clr the winning cells and showing
        the relevant msg) and asking if the player wants another round.
        """
        winner_name = self.__game.get_winner()
        if winner_name == TIE:
            self.__turn_info_lbl["text"] = TIE_MSG
        else:
            winner = self.__convert_name_to_player(winner_name)
            self.__turn_info_lbl[
                "text"] = WINNING_MSG % self.__get_player_letter(winner_name)
            winner.update_score()

            for cell in self.__game.get_win_seq():
                self.__change_circle_color(cell[0], cell[1], WIN_CELLS_CLR)

        self.__another_game = messagebox.askyesno(GAME_OVER, PLAY_AGAIN_MSG)
        self.__parent.destroy()

    def __create_board(self, parent):
        """
        method that is responsible to create the board.
        """
        main_frame = tki.Frame(parent)
        main_frame.pack(side=tki.LEFT)

        board = tki.Frame(main_frame)
        board.pack()
        self.__create_board_cells(board)

    def __create_board_cells(self, parent):
        """
        method that creates all cells of the board (of the gui)
        """
        # cell image
        bg_img = tki.PhotoImage(file=CELL_FRAME_IMG)
        bg_img.image = bg_img
        height = bg_img.height()
        width = bg_img.width()

        # creating each cell
        for i in range(ROWS):
            canvas_row = []
            for j in range(COLUMNS):
                canvas = tki.Canvas(parent, width=width,
                                    height=height,
                                    highlightthickness=0, bg="LightSkyBlue2")
                canvas.create_image(width / 2, height / 2, image=bg_img)
                canvas.grid(row=i, column=j)
                circle = self.__draw_circle(canvas, width / 2, height / 2,
                                            CIRCLE_SIZE, fill="white")

                canvas.bind('<1>', self.__pressed_btn(j))
                canvas.bind('<Enter>', self.__enter_leave_circle(j, True))
                canvas.bind('<Leave>', self.__enter_leave_circle(j, False))

                canvas_row.append((canvas, circle))

            self.__canvas_cells.append(canvas_row)

    def __init_labels(self, parent):
        """
        method that initialises all the labels in the gui.
        :param parent:
        :return:
        """
        self.__init_curr_turn_lbl()
        self.__init_score_lbl(parent)
        self.__init_logo(parent)

    def __init_curr_turn_lbl(self):
        """
        method that initialises the label that shows the curr turn.
        """
        self.__turn_info_lbl[
            "text"] = PLAYER_TURN_MSG % self.__get_player_letter()
        self.__turn_info_lbl['relief'] = 'solid'
        self.__turn_info_lbl['font'] = ('courier', 26)
        self.__turn_info_lbl.pack(side=tki.TOP, padx=30, pady=30)

    def __init_score_lbl(self, parent):
        """
        method that initialises the score labels.
        """
        # score_frame
        score_frame = tki.Frame(parent, relief='solid', bg='red3')
        score_frame.pack(side=tki.TOP, padx=30)
        headline = tki.Label(score_frame, text="SCORE", fg='black', bg='snow2',
                             font=("helvetica", 30, 'bold'))
        headline.pack(side=tki.TOP, pady=10)

        # score labels
        score_a_txt = SCORE_TXT % (PLAYER_A_NAME, self.__player_a.get_score())
        score_a = tki.Label(score_frame, text=score_a_txt, borderwidth=3,
                            relief="solid", font="helvetica",
                            fg=self.__player_a.get_color(), bg='snow2')
        score_a.pack(side=tki.LEFT, padx=5)

        score_b_txt = SCORE_TXT % (PLAYER_B_NAME, self.__player_b.get_score())
        score_b = tki.Label(score_frame, text=score_b_txt, borderwidth=3,
                            relief="solid", font="helvetica",
                            fg=self.__player_b.get_color(), bg='snow2')
        score_b.pack(side=tki.RIGHT, padx=5)

    def __init_logo(self, parent):
        """
        method that initialises the logo.
        """
        logo = tki.PhotoImage(file=LOGO_PNG)
        photo_lbl = tki.Label(parent, image=logo, bg="LightSkyBlue2")
        photo_lbl.image = logo
        photo_lbl.pack(side=tki.TOP, expand='yes')

    def __pressed_btn(self, col):
        """
        method that defines the functionality of the buttons on the board.
        :return: functionality of the buttons
        """

        def btn_click(event=None):
            """
            function that is related to each btn.
            """
            player = self.__get_current_player()
            # play only if this is a user turn.
            if player.get_type() == AI_TYPE or \
                    self.__game.get_winner() is not None:
                return
            self.__make_move(player, col)

        return btn_click

    def __make_move(self, player, col):
        """
        method that makes a move on the board with given player and column.
        :param player: player that made the move.
        :param col: column( the move)
        """
        try:
            if player.get_type() == AI_TYPE:
                self.__parent.update()
                time.sleep(AI_DELAY)

            self.__game.make_move(col)
            row, column = self.__game.get_last_move()
            self.__change_circle_color(row, column, player.get_color())

            # check if the game is over.
            if self.__game.get_winner() is not None:
                self.__finish_game()
            else:
                self.__turn_info_lbl[
                    "text"] = PLAYER_TURN_MSG % self.__get_player_letter()
                self.__turn_manager()
        except ValueError:
            messagebox.showerror(ERROR_TITLE, ERROR_MSG)

    def __draw_circle(self, my_canvas, x, y, r, **kwargs):
        """
        draws the circle on the given canvas.
        :param my_canvas: canvas obj
        :param x: x coordinate (circle center)
        :param y: y coordinate (circle center)
        :param r: circle's radius
        :param kwargs: additional settings
        :return: index of the circle in the canvas
        """
        idx = my_canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        return idx

    def __change_circle_color(self, row, col, color):
        """
        method that gets the circle's coordinates on the board and the wanted
        color and paint it.
        """
        curr_canvas = self.__canvas_cells[row][col][0]
        curr_circle = self.__canvas_cells[row][col][1]
        curr_canvas.itemconfig(curr_circle, fill=color)
        curr_canvas.update()

    def __enter_leave_circle(self, col, is_enter):
        """
        method that defines the functionality of entering or leaving the
        circle.
        :param col: column
        :param is_enter: bool value - True= entering, False=leave.
        :return: function with the relevant functionality.
        """

        def func(event):
            """
            changes the color of the relevant cell.
            """
            player = self.__get_current_player()
            if player.get_type() == AI_TYPE:
                return
            if is_enter:
                color = player.get_color()
            else:
                color = "white"
            col_counter = self.__game.get_column_dict()
            row = ROWS - col_counter[col] - 1
            if row >= 0:
                self.__change_circle_color(row, col, color)

        return func

    def __get_player_letter(self, player_name=None):
        """
        method that returns the letter that represents the given player.
        :param player_name: name (int)
        :return: letter
        """
        if player_name is None:
            player_num = self.__get_current_player().get_name()
        else:
            player_num = player_name
        if player_num == 1:
            return PLAYER_A_NAME
        else:
            return PLAYER_B_NAME

    # public method
    def get_another_game(self):
        """ Getter """
        return self.__another_game
