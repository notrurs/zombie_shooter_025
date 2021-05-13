import pygame

from game.game import Game
from game_object.entities.player import Player
from game_object.entities.bullet import Bullet
from game_object.entities.etwas import Etwas
from game_object.entities.zombie import Zombie
from game_object.landscapes.ground import Ground
from game_object.landscapes.stone import Stone
from game_object.landscapes.palm import Palm

from config import WINDOW_CAPTION
from config import BACKGROUND_COLOR
from config import FRAME_RATE
from config import PLAYER_IMAGE
from config import PLAYER_SPEED
from config import PLAYER_HEALTH
from config import PLAYER_IMMORTALITY_TIME
from config import BULLET_IMAGE
from config import BULLET_SPEED
from config import BULLET_DAMAGE
from config import ZOMBIE_IMAGE
from config import ZOMBIE_SPEED
from config import ZOMBIE_RADIUS_AGR
from config import ZOMBIE_HEALTH
from config import ZOMBIE_DAMAGE
from config import ETWAS_IMAGE
from config import ETWAS_SPEED
from config import ETWAS_RADIUS_AGR
from config import ETWAS_HEALTH
from config import ETWAS_DAMAGE

from config import LEVEL_1


class GameLogic(Game):
    """Класс игровой логики, где связаны все объекты между собой и реализовано их взаимодействие"""
    def __init__(self):
        """
        player - объект игрока
        """
        super().__init__(WINDOW_CAPTION, BACKGROUND_COLOR, FRAME_RATE, LEVEL_1)
        self.player = None
        self.create_objects()

    def create_objects(self):
        """Метод, вызывающий все остальные методы, которые что-то создают"""
        self.create_level()

    def create_level(self):
        """Метод, создающий уровень"""
        with open(LEVEL_1) as f:
            level_objects_list = f.readlines()

        x = y = 0

        level_objects_list = map(lambda string: string.rstrip(), level_objects_list)

        for row in level_objects_list:
            for obj in row:
                self.landscapes.add(Ground(x, y))
                if obj == '-':
                    self.obstacles.add(Stone(x, y))
                elif obj == '+':
                    self.obstacles.add(Palm(x, y))
                elif obj == 'P':
                    self.create_player(x, y)
                elif obj == 'Z':
                    self.create_zombie(x, y)
                elif obj == 'E':
                    self.create_etwas(x, y)
                x += 40
            y += 40
            x = 0

    def create_player(self, x, y):
        """Метод, создающий игрока"""
        player = Player(
            x,
            y,
            PLAYER_IMAGE,
            PLAYER_SPEED,
            PLAYER_HEALTH,
            PLAYER_IMMORTALITY_TIME
        )

        # Список со всеми клавишами на клавиатуре, которые могут быть задействованы игроком
        keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

        # Список со всеми событиями мышки, которые могут быть задейстованы игроком
        mouse_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]

        # Добавляем все клавиши в соответствующие словари
        for key in keys:
            self.keydown_handlers[key].append(player.keydown_handler)
            self.keyup_handlers[key].append(player.keyup_handler)

        # Добавляем все события мышки в словарь
        for event in mouse_events:
            self.mouse_handlers[event].append(player.mouse_handler)

        # Добавляем созданного игрока в группу игровых объектов и в объект игровой логики
        self.player_objects.add(player)
        self.player = player

    def create_zombie(self, x, y):
        """Метод, создающий зомби"""
        zombie = Zombie(
            x,
            y,
            ZOMBIE_IMAGE,
            ZOMBIE_SPEED,
            ZOMBIE_RADIUS_AGR,
            ZOMBIE_HEALTH,
            ZOMBIE_DAMAGE
        )
        self.enemies.add(zombie)
        
    def create_etwas(self, x, y):
        """Метод, создающий нечто"""
        etwas = Etwas(
            x,
            y,
            ETWAS_IMAGE,
            ETWAS_SPEED,
            ETWAS_RADIUS_AGR,
            ETWAS_HEALTH,
            ETWAS_DAMAGE
        )
        self.enemies.add(etwas)

    def handle_bullet(self):
        """Обработчик создания пуль"""
        if self.player.state == 'attack':
            spawn_bullet_x, spawn_bullet_y = self.player.get_barrel_pos()
            bullet = Bullet(
                spawn_bullet_x,
                spawn_bullet_y,
                BULLET_IMAGE,
                BULLET_SPEED,
                BULLET_DAMAGE,
                pygame.mouse.get_pos()
            )
            self.player_bullets.add(bullet)

    def handle_enemy_attack(self):
        """Обработчик атаки врагов"""
        for enemy in self.enemies:
            if pygame.sprite.collide_circle(enemy, self.player):
                enemy.change_state()
                enemy.attack(self.player.rect)
            else:
                enemy.attack(self.player.rect)

    def handle_bullet_with_enemy_collision(self):
        """Обработчик столкновений пуль с врагами"""
        # {'пуля1': [enemy1, enemy2, ...], 'пуля2': [enemy3]}
        dct_bullets = pygame.sprite.groupcollide(self.player_bullets, self.enemies, False, False)
        for bullet, enemies in dct_bullets.items():
            for enemy in enemies:
                enemy.get_damage(bullet.damage)
            bullet.kill()

    def handle_player_with_enemy_collision(self):
        """Обработчик столкновений игрока с врагом"""
        collided_enemy = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in collided_enemy:
            self.player.get_damage(enemy.damage)

    def handle_player_with_obstacles_collision(self):
        """Обработчик столкновений игрока с препятствиями"""
        collided_obstacles = pygame.sprite.spritecollide(self.player, self.obstacles, False)

        if not collided_obstacles:
            self.player.block_moving(None)
        else:
            for obstacle in collided_obstacles:
                if self.player.rect.collidepoint(*obstacle.rect.midleft) and self.player.moving_right:
                    self.player.block_moving('right')
                elif self.player.rect.collidepoint(*obstacle.rect.midright) and self.player.moving_left:
                    self.player.block_moving('left')
                elif self.player.rect.collidepoint(*obstacle.rect.midbottom) and self.player.moving_up:
                    self.player.block_moving('top')
                elif self.player.rect.collidepoint(*obstacle.rect.midtop) and self.player.moving_down:
                    self.player.block_moving('bottom')

    def handle_bullet_with_obstacle_collision(self):
        """Обработчик столкновений пуль с препятствиями"""
        pygame.sprite.groupcollide(self.player_bullets, self.obstacles, True, False)

    def handle_enemy_with_obstacle_collision(self):
        """Обработчик столкновений врагов с препятствиями"""
        # {'враг1': [препятствие1, препятствие2, ...], 'враг2': [препятствие3]}
        dct_colided_obstacles = pygame.sprite.groupcollide(self.enemies, self.obstacles, False, False)
        if not dct_colided_obstacles:
            for enemy in self.enemies:
                enemy.block_moving(None)
        else:
            for enemy, obstacles in dct_colided_obstacles.items():
                for obstacle in obstacles:
                    if enemy.rect.collidepoint(*obstacle.rect.midleft) and enemy.moving_right:
                        enemy.block_moving('right')
                    elif enemy.rect.collidepoint(*obstacle.rect.midright) and enemy.moving_left:
                        enemy.block_moving('left')
                    elif enemy.rect.collidepoint(*obstacle.rect.midbottom) and enemy.moving_up:
                        enemy.block_moving('top')
                    elif enemy.rect.collidepoint(*obstacle.rect.midtop) and enemy.moving_down:
                        enemy.block_moving('bottom')

    def update(self):
        """Запускает все хендлеры и вызывает update родителя"""
        self.handle_bullet()
        self.handle_enemy_attack()
        self.handle_bullet_with_enemy_collision()
        self.handle_player_with_enemy_collision()
        self.handle_player_with_obstacles_collision()
        self.handle_bullet_with_obstacle_collision()
        self.handle_enemy_with_obstacle_collision()
        super().update()


# "Запускатр" игры
if __name__ == '__main__':
    GameLogic().run()
