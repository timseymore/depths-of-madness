import pygame


class MousePointer(object):
    """ The Mouse Pointer Object """
    def __init__(self):
        self.image = pygame.image.load("src/graphics/mouse_cursor.png")
        self.rect = self.image.get_size()
        pygame.mouse.set_visible(False)

    @staticmethod
    def get_pos():
        """ Returns: Tuple (x, y) position of mouse """
        return pygame.mouse.get_pos()

    @staticmethod
    def get_pressed():
        """
        Returns the state of the mouse buttons
        (button1, button2, button3) Boolean values
        """
        return pygame.mouse.get_pressed

    @staticmethod
    def get_focused():
        """ Returns Boolean; True if mouse is active """
        return pygame.mouse.get_focused()
