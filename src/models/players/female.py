import pygame

from src.models.players.player import Player


class Female(Player):
    """ Female is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])

     interp. f = Female(x, y) creates a playable female character where:
              - x is the x coordinate
              - y is the y coordinate
     """

    def __init__(self, x, y):
        """ Constructor method

        - x: int :  x location to spawn
        - y: int :  y location to spawn
        """

        super().__init__(x, y)
        self.image_right = pygame.image.load(r'src/graphics/female_right.png')
        self.image_left = pygame.image.load(r'src/graphics/female_left.png')
        self.image = self.image_right
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.gender = 'female'

    # def switch_img(self, last, new):
    #     """ Switches img based on direction of movement. """
    #
    #     if last.right < new.right:
    #         self.image = pygame.image.load(r'src/graphics/female_right.png')
    #     elif last.left > new.left:
    #         self.image = pygame.image.load(r'src/graphics/female_left.png')
