from time import monotonic
from math import sin
from math import cos
from math import radians

import pygame

from shooter.game_object.entity import Entity
# from game_object.entity import Entity



class Player(Entity):
    """
    Класс игрока. Игрок умеет ходить и стрелять.
    """
    def __init__(self, x, y, image, speed, health, immortality_time):
        """
        speed - скорость игрока
        moving_* - булевые значения, которые сообщают, движется ли персонаж в какую-либо из сторон
        state - состояние игрока ("idle" - ничего не делает, "attack" - атакует)
        health - уровень жизни игрока
        immortality_time - время неуязвимости после получения урона
        last_damage_time - время последнего полученного урона
        """
        super().__init__(x, y, image, speed)
        self.speed = speed
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.collide_bottom = False
        self.state = 'idle'
        self.health = health
        self.immortality_time = immortality_time
        self.last_damage_time = monotonic()  # unix-time timestamp
        self.rad = self.rect.w // 2

    def get_barrel_pos(self):
        """Метод, возвращающий приближенные координаты ствола оружия"""
        x = self.rect.centerx + self.rad * -cos(radians(self.angle))
        y = self.rect.centery + self.rad * -sin(radians(self.angle))
        return x, y

    def block_moving(self, side=None):
        """Метод, сообщающий какой из сторон персонаж коснулся препрятсивя"""
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

    def get_damage(self, damage):
        """Метод, отвечающий за получение игроком урона"""
        cur_damage_time = monotonic()
        if cur_damage_time - self.last_damage_time >= self.immortality_time:
            self.health -= damage
            self.last_damage_time = cur_damage_time
            if self.health <= 0:
                self.kill()

    def keydown_handler(self, key):
        """Метод-обработчик нажатых клавиш"""
        if key == pygame.K_w:
            self.moving_up = True
        elif key == pygame.K_s:
            self.moving_down = True
        elif key == pygame.K_a:
            self.moving_left = True
        elif key == pygame.K_d:
            self.moving_right = True

    def keyup_handler(self, key):
        """Метод-обработчик отжатых клавиш"""
        if key == pygame.K_w:
            self.moving_up = False
        elif key == pygame.K_s:
            self.moving_down = False
        elif key == pygame.K_a:
            self.moving_left = False
        elif key == pygame.K_d:
            self.moving_right = False

    def mouse_handler(self, event_type, event_pos):
        """Метод-обработчик событий мышки"""
        if event_type == pygame.MOUSEMOTION:
            self.rotate(event_pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.state = 'attack'
        elif event_type == pygame.MOUSEBUTTONUP:
            self.state = 'idle'

    def update(self):
        """Метод, отвечающий за изменение объекта (как простанственное, так и визуальное)"""
        dx = dy = 0

        if self.moving_left:
            dx = -self.speed
        if self.moving_right:
            dx = self.speed
        if self.moving_up:
            dy = -self.speed
        if self.moving_down:
            dy = self.speed

        if self.moving_left and self.collide_left:
            dx = 0
        if self.moving_right and self.collide_right:
            dx = 0
        if self.moving_up and self.collide_top:
            dy = 0
        if self.moving_down and self.collide_bottom:
            dy = 0

        self.move(dx, dy)
