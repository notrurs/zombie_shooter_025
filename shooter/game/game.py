import sys
from collections import defaultdict

import pygame


class Game:
    """Класс игры, который содержит в себе основные настроки."""
    def __init__(self, caption, background, frame_rate, level):
        """
        background - задний фон игры
        frame_rate - FPS игры
        clock - нужен для манипулирования fps

        game_objects - список всех игровых объектов
        enemies - группа с врагами
        player_objects - группа со всеми объектами игрока (пока здесь только сам игрок)
        player_bullets - группа со всеми пулями, выпущенными игроком
        landscapes - группа с объектами окружения, с которыми игрок никак не взаимодействует (земля, например)
        obstacles - группа с препятствиями, с которыми игрок игровые персонажи могут столкнуться

        keydown_handlers - словарь для нажатых клавиш с парами 'клавиша': [список методов-хендлеров каждого объекта, которому нужна эта клавиша]
        keyup_handlers - словарь для отжатых клавиш с парами 'клавиша': [список методов-хендлеров каждого объекта, которому нужна эта клавиша]
        mouse_handlers - словарь с событиями мышки с парами 'событие': [список методов-хендлеров каждого объекта, которому нужна мышка]

        width, height - рассчитанные ширина и длина уровня level
        surface - поверхность, на которой отображатся все игровые объекты, её ширина и длина задаются параметрами
        width и height
        """
        pygame.init()
        self.background = background  # pygame.image.load(background)
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()

        self.game_objects = []
        self.enemies = pygame.sprite.Group()
        self.player_objects = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.landscapes = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.keydown_handlers = defaultdict(list)  # {'Клавиша': [handler_key_obj1, handler_key_obj2, ...]}
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = defaultdict(list)

        width, height = self.calc_window_params(level)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

    @staticmethod
    def calc_window_params(level):
        """Рассчитывает ширину и длину уровня"""
        with open(level) as f:
            level_objects_list = f.readlines()

        level_objects_list = list(map(lambda string: string.rstrip(), level_objects_list))

        width = len(max(level_objects_list, key=len)) * 40
        height = len(level_objects_list) * 40
        return width, height

    def start_game(self):
        """Главный игровой метод. Содержит бесконечный цикл, внутри которого работает всё"""
        while True:
            self.handle_events()
            self.game_objects = [*self.landscapes, *self.obstacles, *self.enemies, *self.player_objects, *self.player_bullets]

            self.surface.fill(self.background)
            self.update()
            self.blit(self.surface)
            pygame.display.update()

            self.clock.tick(self.frame_rate)

    def handle_events(self):
        """Главный обработчик игровых событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                for handler in self.mouse_handlers[event.type]:
                    handler(event.type, event.pos)

    def update(self):
        """Метод, обновляющий состояния всех объектов."""
        for obj in self.game_objects:
            obj.update()

    def blit(self, surface):
        """Метод, отображающий все объекты"""
        for obj in self.game_objects:
            obj.blit(surface)

    def run(self):
        """Метод, запускающий игру"""
        self.start_game()
