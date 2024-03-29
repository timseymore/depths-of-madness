import pygame


class Enemy(pygame.sprite.Sprite):
    """ Enemy that the player battles """

    def __init__(self, x, y):
        """ Constructor method

        - x: int : x position to spawn
        - y: int : y position to spawn
        """

        super().__init__()
        self.origin_x = x
        self.origin_y = y
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.platforms = None
        self.player = None
        # TODO: should be a method to set up image for each sub class
        self.image_right = pygame.image.load(r'src/graphics/demon_right.png')
        self.image_left = pygame.image.load(r'src/graphics/demon_left.png')
        self.image = self.image_right
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def switch_img(self):
        """ Switches img based on direction of movement """

        if self.change_x < 0:
            self.image = self.image_left
        elif self.change_x > 0:
            self.image = self.image_right

    def update(self, dt, gravity):
        """ Update the enemy position.

        - dt: int : delta time
        - gravity: int : gravity constant
        """

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
