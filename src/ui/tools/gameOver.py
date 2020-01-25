import pygame

from src.ui.tools.eventBox import EventBox


class GameOver(EventBox):
    """ Event box for end of game by death. """

    def __init__(self, x: int, y: int):
        """ Constructor Method """

        super().__init__(x, y)
        self.image = pygame.image.load(r'src/graphics/game_over.png')
        self.music = r'src/sounds/over_background.wav'
