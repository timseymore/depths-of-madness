import pygame

from ui.tools.colors import Color


class Door(pygame.sprite.Sprite):
    """ The door that clears the current level."""
    text = "A door that exits the level."

    def __init__(self, x, y, width, height):
        """ Constructor Method """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Color.DarkBrown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (5, 40), 3, 1)

    def get_text(self):
        """ Prints description """
        return self.text
