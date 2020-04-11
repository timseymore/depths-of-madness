import pygame


class SpriteGroup(pygame.sprite.Group):
    """ A sprite group list used in game

    used to improve readability and possible changes in implementation
    """

    def __int__(self):
        super().__init__()
