from pathlib import Path

# Настройки путей
_BASE_DIR = Path.cwd()
_RESOURCES_DIR = _BASE_DIR / 'resources'
_IMAGES_DIR = _RESOURCES_DIR / 'images'
_LEVELS_DIR = _RESOURCES_DIR / 'levels'

# Общие настройки
WINDOW_CAPTION = 'Зомби шутер'
FRAME_RATE = 60
BACKGROUND_COLOR = (0, 0, 0)

# Настройки для игрока
PLAYER_IMAGE = _IMAGES_DIR / 'player_min.png'
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_IMMORTALITY_TIME = 1

# Настройки пуль
BULLET_IMAGE = _IMAGES_DIR / 'bullet.png'
BULLET_SPEED = 15
BULLET_DAMAGE = 10

# Настройки зомби
ZOMBIE_IMAGE = _IMAGES_DIR / 'zombie_min.png'
ZOMBIE_SPEED = 2
ZOMBIE_RADIUS_AGR = 70
ZOMBIE_HEALTH = 2000
ZOMBIE_DAMAGE = 40

# Список уровней
LEVEL_1 = _LEVELS_DIR / 'level.txt'

# Объекты окружения
LANDSCAPE_GROUND = _IMAGES_DIR / 'ground.png'
LANDSCAPE_STONE = _IMAGES_DIR / 'new_st'
LANDSCAPE_PALM = _IMAGES_DIR / 'palm-1.png'
