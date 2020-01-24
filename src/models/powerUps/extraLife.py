import pygame

from src.models.powerUps.powerUp import PowerUp


class ExtraLife(PowerUp):
    """ Extra Life Object """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load(r'src/graphics/life.png')
        self.text = "Gives player one extra life."
