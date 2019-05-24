import pygame

from src.models.players.player import Player


class Female(Player):
    """
     Female is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. f = Female(x, y) creates a playable female character where:
              - x is the x coordinate
              - y is the y coordinate
     f = Female(20, 10)  creates a female player at x position 20 and y position 10

     def fn-for-female(f):      Female
         ... f.x                Integer[0, WIDTH]
             f.y                Integer[0, HEIGHT]
     """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)
        self.image = pygame.image.load("graphics\\female_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.gender = "female"

    def switch_img(self, last, new):
        """ Switches img based on direction of movement. """
        if last.right < new.right:
            self.image = pygame.image.load("graphics\\female_right.png")
        elif last.left > new.left:
            self.image = pygame.image.load("graphics\\female_left.png")
