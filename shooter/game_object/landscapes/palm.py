from shooter.game_object.landscape import Landscape
from shooter.config import LANDSCAPE_PALM


class Ground(Landscape):
    """Класс пальмы"""
    def __init__(self, x, y, image=LANDSCAPE_PALM):
        super().__init__(x, y, image)
