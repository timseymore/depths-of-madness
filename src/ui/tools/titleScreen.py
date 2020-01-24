import pygame

from src.ui.tools.eventBox import EventBox


class TitleScreen(EventBox):
    """ Event box for the title screen. """

    def __init__(self, x: int, y: int):
        """ Constructor Method """

        super().__init__(x, y)

        self.image = pygame.image.load(r'src/graphics/menu.png')
        self.music = r'src/sounds/menu_background.wav'
