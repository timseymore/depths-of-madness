import pygame


class Platform(pygame.sprite.Sprite):
    """Platform that floats or moves in the game."""
    def __init__(self, x, y):
        """ Constructor Method """
        super().__init__()

        self.image = pygame.image.load("graphics/platform.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

        self.change_x = 0
        self.change_y = 0

        self.min_x = 25
        self.max_x = 775
        self.min_y = 25
        self.max_y = 575

        self.walls = None

    def change_bounds(self, min_x, max_x, min_y, max_y):
        """ Change the upper and lower bounds on x and y"""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def change_speed(self, x, y):
        """ Change the speed of the platform. """
        self.change_x += x
        self.change_y += y

    def update(self, dt, gravity):
        """ Update the platform position. """
        # Move left/right
        if self.min_x <= self.rect.x <= self.max_x:
            self.rect.x += self.change_x
        else:
            self.change_x *= -1

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of block
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.change_x *= -1

        # Move up/down
        if self.min_y < self.rect.y < self.max_y:
            self.rect.y += self.change_y
        else:
            self.change_y *= -1
            self.rect.y += self.change_y

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving down, set our bottom side to the top side of block
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
            else:
                # Otherwise if we are moving up, do the opposite.
                self.rect.top = block.rect.bottom
                self.change_y *= -1
