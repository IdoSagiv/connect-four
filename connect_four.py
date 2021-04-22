import tkinter as tki
from ConnectFour.Game.game import Game
from ConnectFour.Game.player import Player
from ConnectFour.gui import Gui


class MyApp:
    """
    class that defines an app object. this object can get user preferences
     (by using the init window) and can initialize game.
    """

    def __init__(self):
        """
        constructor of the class.
        """
        self.__score_a = 0
        self.__score_b = 0
        self.__keep_playing = True

    # public method
    def play(self):
        """
        starts a game. starts new game init window while keep playing is true.
        """
        while self.__keep_playing:
            self.__score_a, self.__score_b = self.__init_window(self.__score_a,
                                                                self.__score_b)

    # private methods
    def __init_player_frame(self, parent, player_name):
        """
        method that initialises player frame in the init window.
        this frame includes options of picking color and type of the player.
        """
        frame = tki.Frame(parent)
        frame.pack(side=tki.LEFT)
        player_type = tki.IntVar(parent, 1)
        tki.Label(frame, text="Player " + player_name).pack(side=tki.TOP)
        tki.Radiobutton(frame,
                        text="user",
                        padx=20,
                        variable=player_type,
                        value=1).pack(anchor=tki.W)
        tki.Radiobutton(frame,
                        text="computer",
                        padx=20,
                        variable=player_type,
                        value=2).pack(anchor=tki.W)

        color = tki.StringVar()
        color.set("blue")
        if player_name == "A":
            color.set("red")

        choose_clr = tki.OptionMenu(frame, color, "red", "blue", "green",
                                    "orange", "purple", "black")
        choose_clr.pack(side=tki.BOTTOM)

        return player_type, color

    def __init_window(self, score_a, score_b):
        """
        method that creates the init window, that gets the settings of the
        game from the user.
        """
        init_window = tki.Tk(None, None, "settings")
        init_window.resizable(width=False, height=False)

        confirm_btn = tki.Button(init_window, text="Start")
        confirm_btn.pack(side=tki.BOTTOM)

        a_type, a_color = self.__init_player_frame(init_window, "A")
        b_type, b_color = self.__init_player_frame(init_window, "B")
        player_a = Player(1, score_a)
        player_b = Player(2, score_b)

        confirm_btn.bind('<1>', self.__start_game(init_window, player_a,
                                                  a_type, a_color, player_b,
                                                  b_type, b_color))

        init_window.protocol("WM_DELETE_WINDOW",
                             self.__terminate_game(init_window))
        init_window.mainloop()

        return player_a.get_score(), player_b.get_score()

    def __terminate_game(self, parent):
        """
        defines the functionality of terminating game, to bind it with
        exit button.
        :return: function to bind to the btn
        """

        def terminate():
            """
            functionality of the btn
            """
            parent.destroy()
            self.__keep_playing = False

        return terminate

    def __start_game(self, parent, player_a, a_type, a_color, player_b, b_type,
                     b_color):
        """
        method that gets all the settings of the new game and defines the
        functionality of starts new game button.
        :return: function to bind to the btn
        """

        def start(event):
            """
            functionality of the btn
            """
            parent.destroy()
            player_a.set_color(a_color.get())
            player_a.set_type(a_type.get())

            player_b.set_color(b_color.get())
            player_b.set_type(b_type.get())

            main_window = tki.Tk(None, None, "4 in a row")
            main_window.resizable(width=False, height=False)
            my_game = Game()
            gui = Gui(main_window, my_game, player_a, player_b)
            main_window.mainloop()
            self.__keep_playing = gui.get_another_game()

        return start


if __name__ == '__main__':
    app = MyApp()
    app.play()
