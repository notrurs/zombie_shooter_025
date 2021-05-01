from shooter.game_object.landscape import Landscape
from shooter.config import LANDSCAPE_GROUND


class Ground(Landscape):
    """Класс земли"""
    def __init__(self, x, y, image=LANDSCAPE_GROUND):
        super().__init__(x, y, image)
