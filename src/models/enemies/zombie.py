from src.models.enemies.enemy import *


class Zombie(Enemy):
    """A Zombie Enemy Class"""

    def __init__(self, x, y):
        """ Constructor method """

        super().__init__(x, y)
        self.image = pygame.image.load(r'src/graphics/zombie_right.png')
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """

        if self.change_x < 0:
            self.image = pygame.image.load(r'src/graphics/zombie_left.png')
        elif self.change_x > 0:
            self.image = pygame.image.load(r'src/graphics/zombie_right.png')
