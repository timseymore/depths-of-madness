import pygame

from ui.tools.eventBox import EventBox


class TitleScreen(EventBox):
    """ Event box for the title screen. """
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__(x, y)

        self.image = pygame.image.load('graphics/menu.png')
        self.music = r'sounds\menu_background.wav'