
class EventBox(object):
    """ A pop up box with text describing events. """

    def __init__(self, x: int, y: int):
        """ Constructor Method """

        self.x = x
        self.y = y
        self.image = None
        self.music = None
