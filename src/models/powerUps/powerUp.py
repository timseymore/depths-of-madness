import pygame


class PowerUp(pygame.sprite.Sprite):
    """ Game object with positive effect on character """

    def __init__(self, x: int, y: int):
        """ Constructor """

        super().__init__()
        self.image = pygame.image.load(r'src/graphics/power_up.png')
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())
        self.text = "A powerful upgrade."
        self.sound = r'src/sounds/power_up.wav'

    def get_x(self) -> int:
        """ Returns current x position."""

        return self.rect.x

    def get_y(self) -> int:
        """ Returns current y position. """

        return self.rect.y

    def get_text(self) -> str:
        """ Returns description text """

        return self.text
