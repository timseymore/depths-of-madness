from src.models.enemies.enemy import Enemy


class Demon(Enemy):
    """ A Default Demon Enemy Class """

    def __init__(self, x, y):
        """ Constructor method

        - x: int : x position to spawn
        - y: int : y position to spawn
        """

        super().__init__(x, y)
