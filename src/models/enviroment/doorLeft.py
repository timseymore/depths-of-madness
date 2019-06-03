import pygame

from ui.tools.colors import Color
from models.enviroment.door import Door


class DoorLeft(Door):
    """ A door that appears on the left side of screen. """
    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__(x, y, width, height)
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Brown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (width - 5, 40), 5, 2)
