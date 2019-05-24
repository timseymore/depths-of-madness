import pygame


class Enemy(pygame.sprite.Sprite):
    """ This class represents an enemy that the player
    battles. """
    def __init__(self, x, y):
        """
        Constructor method
        :param x: x location to spawn
        :param y: y location to spawn
        """
        super().__init__()

        # Class states
        self.walls = None
        self.platforms = None
        self.player = None

        self.change_x = 0
        self.change_y = 0

        self.origin_x = x
        self.origin_y = y

        self.image = pygame.image.load("graphics/demon_right.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """
        if self.change_x < 0:
            self.image = pygame.image.load("graphics/demon_left.png")
        elif self.change_x > 0:
            self.image = pygame.image.load("graphics/demon_right.png")

    def update(self, dt, gravity):
        """ Update the enemy position. """
        # Move left/right
        last = self.rect.copy()
        self.rect.x += self.change_x
        self.switch_img()
        new = self.rect

        for cell in pygame.sprite.spritecollide(self, self.walls, False):
            cell = cell.rect
            if last.right <= cell.left < new.right:
                new.right = cell.left
                self.change_x *= -1
            if new.left < cell.right <= last.left:
                new.left = cell.right
                self.change_x *= -1
            if last.bottom <= cell.top < new.bottom:
                new.bottom = cell.top
            if new.top < cell.bottom <= last.top:
                new.top = cell.bottom
