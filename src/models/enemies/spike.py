from src.models.enemies.enemy import *


class Spike(Enemy):
    """ A Spike Block Class """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)

        # Set Spike image
        self.image = pygame.image.load(r'src/graphics/spikes.png')
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
