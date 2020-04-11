import pygame

from src.ui.tools.colors import Color


class Door(pygame.sprite.Sprite):
    """ The door that clears the current level """

    def __init__(self, x, y, width, height, exit_level):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        - width: int : width of door
        - height: int : height of door
        - exit_level: Level : level door will exit to
        """

        super().__init__()
        self.exit_level = exit_level
        self.text = 'A door that exits to level ' + str(self.exit_level)
        self.image = pygame.Surface([width, height])
        self.image.fill(Color.DarkBrown)
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        pygame.draw.circle(self.image, Color.Black, (5, 40), 3, 1)

    def get_text(self):
        """ Prints description """

        return self.text
