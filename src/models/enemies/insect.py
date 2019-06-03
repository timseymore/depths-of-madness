from models.enemies.enemy import *


class Insect(Enemy):
    """ An Insect Enemy Class """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__(x, y)

        # Set Insect image
        self.image = pygame.image.load("graphics/insect_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """
        if self.change_x < 0:
            self.image = pygame.image.load("graphics/insect_left.png")
        elif self.change_x > 0:
            self.image = pygame.image.load("graphics/insect_right.png")
