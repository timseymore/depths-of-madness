import pygame

from src.ui.tools.colors import Color
from src.models.enviroment.door import Door


class DoorLeft(Door):
    """ A door that appears on the left side of screen. """

    def __init__(self, x, y, width, height, exit_level):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        - width: int : width of door
        - height: int : height of door
        - exit_level: Level : level door will exit to
        """

        super().__init__(x, y, width, height, exit_level)
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Brown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (width - 5, 40), 5, 2)
