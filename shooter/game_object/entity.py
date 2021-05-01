from math import atan2
from math import degrees

import pygame
from pygame.transform import rotate


class Entity(pygame.sprite.Sprite):
    """Класс игровой сущности"""
    def __init__(self, x, y, image, speed):
        """
        image - картинка игрового объекта, которая отображается на экране
        original_image - "картинка-эталон", которую вращает метод rotate() для предотвращения искажений
        rect - прямоугольник, созданный на основе картинке
        speed - скорость перемещения игрового объекта
        """
        super().__init__()
        self.image = pygame.image.load(image)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = 0

    def move(self, dx, dy):
        """Перемещает игровой объект"""
        self.rect.move_ip(dx, dy)

    def update(self):
        """Метод, отвечающий за изменение объекта (как простанственное, так и визуальное)"""
        self.move(*self.speed)

    def blit(self, surface):
        """Отображает игровой объект"""
        surface.blit(self.image, self.rect)

    def rotate(self, target):
        """Поворачивает игровой объект в сторону target"""
        angle = atan2(target[1] - self.rect.centery, target[0] - self.rect.centerx)  # Радианы
        angle = degrees(angle)  # Углы
        self.angle = 180 + angle
        self.image = rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)
