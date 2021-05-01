from math import atan2
from math import degrees
from math import sin
from math import cos

from pygame.transform import rotate

from shooter.game_object.entity import Entity


class Zombie(Entity):
    """Класс зомби. Его атака заключается в том, что он просто поворачивается к цели и идёт в её сторону"""
    def __init__(self, x, y, image, speed, radius, health, damage):
        """
        speed - содержит дельты скоростей по оси Х и Y
        const_speed - скорость зомби
        state - состояние зомби
        radius - радиус, в рамках которого зомби может заметить игрока
        health - уровень здоровья зомби
        damage - урон зомби
        moving_* - булевые значения, которые сообщают, движется ли зомби в какую-либо из сторон
        collide_* - булевые значения, которые сообщают, касается ли зомби какой-либо из сторон какого-либо препятствия
        angle - угол поворота зомби
        """
        super().__init__(x, y, image, speed)
        self.speed = (0, 0)
        self.const_speed = speed
        self.state = 'idle'
        self.radius = radius
        self.health = health
        self.damage = damage
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.collide_bottom = False
        self.angle = 0

    def get_damage(self, damage):
        """Метод, отвечающий за нанесение урона по зомби"""
        self.health -= damage
        self.change_state()
        if self.health <= 0:
            self.kill()

    def rotate(self, target):
        """Метод, отвечающий за поворот зомби"""
        if self.state == 'attack':
            angle = atan2(target[1] - self.rect.y, target[0] - self.rect.x)

            dx = round(self.const_speed * cos(abs(angle)))
            if target[1] < self.rect.y:
                dy = -round(self.const_speed * sin(abs(angle)))
            else:
                dy = round(self.const_speed * sin(abs(angle)))

            angle = degrees(angle)
            self.angle = 180 + angle
            self.image = rotate(self.original_image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.speed = (dx, dy)

    def set_moving(self):
        """Устанавливает направление движения в зависимости от угла поворота"""
        if 10 <= self.angle < 80:
            self.moving_up = True
            self.moving_left = True
            self.moving_right = False
            self.moving_down = False
        elif 80 <= self.angle < 100:
            self.moving_up = True
            self.moving_left = False
            self.moving_right = False
            self.moving_down = False
        elif 100 <= self.angle < 170:
            self.moving_up = True
            self.moving_left = False
            self.moving_right = True
            self.moving_down = False
        elif 170 <= self.angle < 190:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True
            self.moving_down = False
        elif 190 <= self.angle < 260:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True
            self.moving_down = True
        elif 260 <= self.angle < 280:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = False
            self.moving_down = True
        elif 280 <= self.angle < 350:
            self.moving_up = False
            self.moving_left = True
            self.moving_right = False
            self.moving_down = True
        else:
            self.moving_up = False
            self.moving_left = True
            self.moving_right = False
            self.moving_down = False

    def block_moving(self, side=None):
        """Метод, сообщающий какой из сторон зомби коснулся препрятсивя"""
        if side == 'left':
            self.collide_left = True
        elif side == 'right':
            self.collide_right = True
        elif side == 'top':
            self.collide_top = True
        elif side == 'bottom':
            self.collide_bottom = True
        else:
            self.collide_left = self.collide_right = self.collide_top = self.collide_bottom = False

    def attack(self, target):
        """Начинает атаку"""
        if self.state == 'attack':
            self.rotate(target)

    def change_state(self):
        """Меняет состояние с "ничего не делать" на "атаковать" """
        if self.state == 'idle':
            self.state = 'attack'

    def update(self):
        """Отвечает за передвижение зомби"""
        if self.state == 'attack':
            self.set_moving()
            dx, dy = self.speed
            if self.moving_left and self.collide_left:
                dx = 0
            if self.moving_right and self.collide_right:
                dx = 0
            if self.moving_up and self.collide_top:
                dy = 0
            if self.moving_down and self.collide_bottom:
                dy = 0

            self.move(dx, dy)
            self.block_moving(None)
        elif self.state == 'idle':
            self.speed = (0, 0)
            self.move(*self.speed)
