import pygame
from player import Player
from bullet import Bullet

# Инициализация PyGame
pygame.init()

# Настройки экрана и FPS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Небесный бой")

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание игровых объектов
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

# Игровой цикл
running = True
while running:
    # Контролируем частоту кадров
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление игровой логики
    all_sprites.update()

    # Автоматическая стрельба
    # Этот блок кода будет вызываться каждый кадр
    # и игрок будет стрелять, если прошло достаточно времени
    new_bullet = player.shoot()
    if new_bullet:
        all_sprites.add(new_bullet)
        bullets.add(new_bullet)

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

# Выход из игры
pygame.quit()