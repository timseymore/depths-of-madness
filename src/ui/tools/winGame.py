import pygame

from src.ui.tools.eventBox import EventBox


class WinGame(EventBox):
    """ Event box for clearing the level / win game. """

    def __init__(self, x, y):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        """

        super().__init__(x, y)
        self.image = pygame.image.load(r'src/graphics/win_game.png')
        self.music = r'src/sounds/win_background.wav'
