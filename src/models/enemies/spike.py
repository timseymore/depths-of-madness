from src.models.enemies.enemy import *


class Spike(Enemy):
    """ A Spike Block Class """

    def __init__(self, x, y):
        """ Constructor method """

        super().__init__(x, y)
        self.image_right = pygame.image.load(r'src/graphics/spikes.png')
        self.image_left = self.image_right
        self.image = self.image_right
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
