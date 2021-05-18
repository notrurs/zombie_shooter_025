from shooter.game_object.landscape import Landscape
from shooter.config import LANDSCAPE_GROUND
from shooter.config import LANDSCAPE_GROUND2


class Ground(Landscape):
    """Класс земли"""
    def __init__(self, x, y, image=LANDSCAPE_GROUND):
        super().__init__(x, y, image)
        
class Mentol(Landscape):
    """Класс земли"""
    def __init__(self, x, y, image=LANDSCAPE_GROUND2):
        super().__init__(x, y, image)        
