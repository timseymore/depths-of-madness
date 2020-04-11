import pygame


class PowerUp(pygame.sprite.Sprite):
    """ Game object with positive effect on character """

    def __init__(self, x, y):
        """ Constructor

        - x: int : x position
        - y: int : y position
        """

        super().__init__()
        self.image = pygame.image.load(r'src/graphics/power_up.png')
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.text = 'A powerful upgrade.'
        self.sound = r'src/sounds/power_up.wav'

    def get_x(self):
        """ Returns current x position."""

        return self.rect.x

    def get_y(self):
        """ Returns current y position. """

        return self.rect.y

    def get_text(self):
        """ Returns description text """

        return self.text
