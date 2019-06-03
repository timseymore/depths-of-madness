import pygame

from models.powerups.powerUp import PowerUp


class ExtraLife(PowerUp):
    """ Extra Life Object """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("graphics/life.png")
        self.text = "Gives player one extra life."