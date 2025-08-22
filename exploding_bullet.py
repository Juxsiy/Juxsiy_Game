import pygame
import math
from enemy_bullet import *

# Константы
EXPLODING_BULLET_SPEED = 3
EXPLOSION_TIME = 30  # Время в кадрах до взрыва
EXPLOSION_BULLETS = 8  # Количество снарядов при взрыве
BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_COLOR = (200, 200, 0)  # Желтый

class ExplodingBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y, all_sprites, enemy_bullets):
        super().__init__()
        
        # Создание изображения
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        
        # Позиционирование пули
        self.rect.centerx = x
        self.rect.top = y
        
        # Параметры движения и взрыва
        self.speed_y = speed_y
        self.life_time = 0
        
        # Группы спрайтов для создания дочерних пуль
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets

    def update(self):
        """Обновление позиции пули и проверка на взрыв"""
        # Движение пули
        self.rect.y += self.speed_y
        self.life_time += 1

        # Проверка времени до взрыва
        if self.life_time > EXPLOSION_TIME:
            self.explode()
            self.kill()
            return

        # Проверка границ экрана
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        
        if (self.rect.top > screen_height or
            self.rect.bottom < 0 or
            self.rect.right < 0 or
            self.rect.left > screen_width):
            self.kill()

    def explode(self):
        """Создание веера дочерних пуль при взрыве"""
        for i in range(EXPLOSION_BULLETS):
            # Расчет угла и скорости для каждой пули
            angle = 360 / EXPLOSION_BULLETS * i
            rad_angle = math.radians(angle)
            
            speed_x = math.cos(rad_angle) * ENEMY_BULLET_SPEED
            speed_y = math.sin(rad_angle) * ENEMY_BULLET_SPEED
            
            # Создание и добавление дочерней пули
            new_bullet = EnemyBullet(
                self.rect.centerx, 
                self.rect.centery, 
                speed_x, 
                speed_y
            )
            
            self.all_sprites.add(new_bullet)
            self.enemy_bullets.add(new_bullet)