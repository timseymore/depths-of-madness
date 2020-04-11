import pygame


class Platform(pygame.sprite.Sprite):
    """Platform that floats or moves in the game."""

    def __init__(self, x, y, x_speed, y_speed, min_x, max_x, min_y, max_y):
        """ Constructor Method

        - x: int : x position of platform
        - y: int : y position of platform
        - x_speed: int : speed at which platform moves left/right
        - y_speed: int : speed at which platform moves up/down
        - min_x: int : lower x bound
        - max_x: int : upper x bound
        - min_y: int : lower y bound
        - max_y: int : upper y bound
        """

        super().__init__()
        self.image = pygame.image.load(r'src/graphics/platform.png')
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.walls = None
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def change_bounds(self, min_x, max_x, min_y, max_y):
        """ Change the upper and lower bounds on x and y

        - min_x: int : new limit for left directional movement
        - max_x: int : new limit for right directional movement
        - min_y: int : new limit for upward directional movement
        - max_y: int : new limit for downward directional movement
        """

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def change_speed(self, x, y):
        """ Change the speed of the platform.

        - x: int : new left/right speed
        - y: int : new up/down speed
        """

        self.x_speed = x
        self.y_speed = y

    def update(self, dt, gravity):
        """ Update the platform position.

        - dt: int : delta time
        - gravity: int : gravity constant
        """

        self.handle_left_right()
        self.handle_up_down()

    def handle_left_right(self):
        """ Handle left and right movement and collisions """

        self.move_left_right()
        self.check_left_right()

    def move_left_right(self):
        """ Move platform left and right """

        self.rect.x = self.move(self.min_x, self.max_x, self.rect.x, self.x_speed)

    def check_left_right(self):
        """ Check for left and right collisions """

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

    def handle_up_down(self):
        """ Handle the up and down movement of the platform """

        self.move_up_down()
        self.check_up_down()

    def move_up_down(self):
        """ Move the platform up and down ignoring any objects """

        if self.min_y <= self.rect.y <= self.max_y:
            self.rect.y += self.y_speed
        else:
            self.y_speed *= -1
            self.rect.y += self.y_speed

    def check_up_down(self):
        """ Change platform direction and position if collision is detected

            NOTE: position should be reset to just outside of colliding object
                  combined with change in direction, platform will be safe to move next tick
        """

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            print('platform collision')
            # If we are moving down, set our bottom side to the top side of block
            if self.y_speed < 0:
                print('moving down')
                self.rect.bottom = block.rect.top
                self.y_speed *= -1
            else:
                print('moving up')
                # Otherwise if we are moving up, do the opposite.
                self.rect.top = block.rect.bottom
                self.y_speed *= -1

    @staticmethod
    def move(lower_bound, upper_bound, pos, velocity, vertical=False):
        """ move platform within given bounds

         - lower_bound: int : lower limit of movement
         - upper_bound: int : upper limit of movement
         - pos: (int, int) : current position
         - velocity: int : rate of change in position
         - vertical: bool : True if moving vertically, False by default
        Return: new position (int, int)
        """
        
        if lower_bound <= pos <= upper_bound:
            pos += velocity
        else:
            velocity *= -1
            if vertical:
                pos += velocity
        return pos
