import pygame

from ui.tools.eventBox import EventBox


class GameOver(EventBox):
    """ Event box for end of game by death. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('graphics/game_over.png')
        self.music = r'sounds\over_background.wav'