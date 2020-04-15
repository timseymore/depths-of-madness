import pygame


class CoinIcon(object):
    """ An icon representing the 'coins' object """

    def __init__(self, x, y):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        """

        self.x = x
        self.y = y
        self.image = pygame.image.load(r'src/graphics/coin_icon.png')
        self.text = "An icon representing the player's coins."

    def get_text(self):
        """ Returns description text"""

        return self.text
