from math import atan2
from math import degrees
from math import sin
from math import cos

from pygame.transform import rotate
from pygame.transform import scale

from shooter.game_object.entity import Entity


class Bullet(Entity):
    """Класс пули"""
    def __init__(self, x, y, image, speed, damage, target):
        """
        speed - скорость пули
        damage - урон пули
        """
        super().__init__(x, y, image, speed)
        self.speed = speed
        self.damage = damage
        self.image = scale(self.image, (int(self.image.get_width() * 0.7), int(self.image.get_height() * 0.7)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_image = self.image.copy()
        self.rotate(target)

    def rotate(self, target):
        """Метод, отвечающий за поворот пули и задающий вектор перемещения (dx, dy)"""
        angle = atan2(target[1] - self.rect.centery, target[0] - self.rect.centerx)

        dx = round(self.speed * cos(abs(angle)))
        if target[1] < self.rect.centery:
            dy = -round(self.speed * sin(abs(angle)))
        else:
            dy = round(self.speed * sin(abs(angle)))

        angle = degrees(angle)
        self.image = rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = (dx, dy)
