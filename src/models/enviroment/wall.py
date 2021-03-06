import pygame

from src.ui.tools.colors import Color


class Wall(pygame.sprite.Sprite):
    """ A wall that the player can run into. """

    def __init__(self, x, y, width, height):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        - width: int : width of block
        - height: int : height of block
        """

        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.Mist)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
