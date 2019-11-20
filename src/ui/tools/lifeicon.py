import pygame


class LifeIcon(object):
    """
    An icon representing the 'player life' object
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"graphics/life_icon.png")
        self.text = "An icon representing the player's lives."

    def get_text(self):
        """ Prints description """
        return self.text
