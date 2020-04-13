class EventBox(object):
    """ A pop up box with text describing events. """

    def __init__(self, x, y):
        """ Constructor Method

        - x: int : x position
        - y: int : y position
        """

        self.x = x
        self.y = y
        self.image = None
        self.music = None
