from src.models.players.player import Player


class Male(Player):
    """ Male is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])

     interp. m = Male(x, y) creates a playable male character where:
              - x is the x coordinate
              - y is the y coordinate
     """

    def __init__(self, x, y):
        """ Constructor method

        - x: int :  x location to spawn
        - y: int :  y location to spawn
        """

        super().__init__(x, y)
        self.gender = 'male'
