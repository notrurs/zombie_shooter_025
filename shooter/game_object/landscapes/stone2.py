from shooter.game_object.landscape import Landscape
from shooter.config import LANDSCAPE_STONE2


class Stone2(Landscape):
    """Класс камня2"""
    def __init__(self, x, y, image=LANDSCAPE_STONE2):
        super().__init__(x, y, image)