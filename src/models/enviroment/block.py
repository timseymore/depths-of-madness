import pygame

from src.models.enviroment.wall import Wall


class Block(Wall):
    """ A stone block to build a wall."""
    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__(x, y, width, height)

        self.image = pygame.image.load("graphics/stone.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
