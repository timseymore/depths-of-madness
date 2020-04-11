from src.models.enemies.enemy import *


class Insect(Enemy):
    """ An Insect Enemy Class """

    def __init__(self, x, y):
        """ Constructor method """

        super().__init__(x, y)
        self.image_right = pygame.image.load(r'src/graphics/insect_right.png')
        self.image_left = pygame.image.load(r'src/graphics/insect_left.png')
        self.image = self.image_right
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
