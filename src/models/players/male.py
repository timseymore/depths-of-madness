import pygame

from src.models.players.player import Player


class Male(Player):
    """
     Male is a Player(Integer[0, WIDTH], Integer[0, HEIGHT])
     interp. m = Male(x, y) creates a playable male character where:
              - x is the x coordinate
              - y is the y coordinate
     m = Male(20, 10)  creates a male player at x position 20 and y position 10

     def fn-for-male(m):        Male
         ... m.x                Integer[0, WIDTH]
             m.y                Integer[0, HEIGHT]
     """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(r"src/graphics/male_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.gender = "male"
