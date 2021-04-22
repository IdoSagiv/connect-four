class Player:
    """
    class that defines players objects. each Game object has 2 players that has
    the following fields and methods.
    """

    def __init__(self, name, score, color="red", player_type=None):
        """
        constructor of player object.
        :param name: player name (1 or 2)
        :param score: the score of the player
        :param color: the player's color
        :param player_type: 1 for user 2 for AI
        """
        self.__name = name
        self.__type = player_type
        self.__color = color
        self.__score = score

    # getters
    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_color(self):
        return self.__color

    def get_score(self):
        return self.__score

    # setters
    def set_type(self, player_type):
        self.__type = player_type

    def set_color(self, player_color):
        self.__color = player_color

    def update_score(self):
        """
        method that updates the player's score (adds 1)
        """
        self.__score += 1
