import pygame


class Platform(pygame.sprite.Sprite):
    """Platform that floats or moves in the game."""

    def __init__(self, x, y):
        """ Constructor Method
             - x: x position of platform
             - y: y position of platform
        """
        super().__init__()
        self.image = pygame.image.load("src/graphics/platform.png")
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.walls = None
        self.x_speed = 0
        self.y_speed = 0
        # TODO should be using game constants instead of hard values
        self.min_x = 25
        self.max_x = 775
        self.min_y = 0
        self.max_y = 575

    def change_bounds(self, min_x, max_x, min_y, max_y):
        """ Change the upper and lower bounds on x and y
             - min_x: new limit for left directional movement
             - max_x: new limit for right directional movement
             - min_y: new limit for upward directional movement
             - max_y: new limit for downward directional movement
        """
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def change_speed(self, x, y):
        """ Change the speed of the platform.
             - x: new left/right speed
             - y: new up/down speed
        """
        self.x_speed += x
        self.y_speed += y

    def update(self, dt, gravity):
        """ Update the platform position. """
        self.handle_left_right()
        self.handle_up_down()

    def handle_left_right(self):
        self.move_left_right()
        self.check_left_right()

    def move_left_right(self):
        self.rect.x = self.move(self.min_x, self.max_x, self.rect.x, self.x_speed)

    def check_left_right(self):
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of block
            if self.x_speed > 0:
                self.rect.right = block.rect.left
                self.x_speed *= -1
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.x_speed *= -1

    # TODO: find and fix bug in vertically moving platform ; remove all print statements when fully tested
    def handle_up_down(self):
        """ Handle the up and down movement of the platform """
        self.move_up_down()
        self.check_up_down()

    def move_up_down(self):
        """ Move the platform up and down ignoring any objects """
        self.rect.y = self.move(self.min_y, self.max_y, self.rect.y, self.y_speed, True)

    def check_up_down(self):
        """ Change platform direction and position if collision is detected
            NOTE: position should be reset to just outside of colliding object
                  combined with change in direction, platform will be safe to move next tick
        """
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            print("platform collision")
            # If we are moving down, set our bottom side to the top side of block
            if self.y_speed < 0:
                print("moving down")
                self.rect.bottom = block.rect.top
                self.y_speed *= -1
            else:
                print("moving up")
                # Otherwise if we are moving up, do the opposite.
                self.rect.top = block.rect.bottom
                self.y_speed *= -1

    @staticmethod
    def move(lower_bound, upper_bound, pos, velocity, vertical=False):
        """
        move platform within given bounds
         - lower_bound: lower limit of movement
         - upper_bound: upper limit of movement
         - pos: current position
         - velocity: rate of change in position
         - vertical: True if moving vertically, False by default
        returns: new position
        """
        if lower_bound <= pos <= upper_bound:
            print("platform in bounds")
            pos += velocity
        else:
            print("platform out of bounds")
            velocity *= -1

            if vertical:
                print("vertical platform")
                pos += velocity

        return pos
