import pygame

from src.models.powerUps.powerUp import PowerUp


class Coin(PowerUp):
    """ Coin Power Up Object """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(r"graphics/coin.png")
        self.text = "Used for extra exp points."
