import pygame

from ui.tools.eventBox import EventBox


class WinGame(EventBox):
    """ Event box for clearing the level / win game. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('graphics/win_game.png')
        self.music = r'sounds\win_background.wav'
