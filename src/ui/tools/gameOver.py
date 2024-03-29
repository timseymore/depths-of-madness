import pygame

from src.ui.tools.eventBox import EventBox


class GameOver(EventBox):
    """ Event box for end of game by death. """

    def __init__(self, x, y):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        """

        super().__init__(x, y)
        self.image = pygame.image.load(r'src/graphics/game_over.png')
        self.music = r'src/sounds/over_background.wav'
