import pygame
import random
import math
from enemy_bullet import *
from exploding_bullet import ExplodingBullet

# Константы
BOSS_SPEED_X = 3
BOSS_SPEED_Y = 1
INITIAL_ATTACK_COOLDOWN = 1500  # мс между атаками
BULLETS_PER_RAPID_FIRE = 5
RAPID_FIRE_DELAY = 150  # мс между выстрелами в очереди
MIN_ATTACK_COOLDOWN = 500  # минимальная задержка атаки

class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, all_sprites, enemy_bullets, player):
        super().__init__()
        
        # Создание изображения
        self.image = pygame.image.load('boss.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.top = 20
        
        # Параметры движения
        self.screen_width = screen_width
        self.initial_y = self.rect.y
        self.speed_x = BOSS_SPEED_X
        self.speed_y = BOSS_SPEED_Y
        
        # Ссылки на группы и игрока
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets
        self.player = player
        
        # Система атак
        self.last_attack = pygame.time.get_ticks()
        self.attack_types = [
            self.single_shot_center,
            self.single_shot_sides,
            self.single_shot_center_and_sides,
            self.spread_shot,
            self.exploding_bullet_shot,
            self.rapid_fire_start
        ]
        
        # Состояние очереди выстрелов
        self.rapid_fire_state = 0
        self.rapid_fire_last_shot = pygame.time.get_ticks()

    def update(self):
        """Обновление позиции и логики атак босса"""
        # Движение босса
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Отскок от границ экрана
        self._handle_border_collision()
        
        # Обработка очереди выстрелов
        if self.rapid_fire_state > 0:
            self.rapid_fire_state_machine()
            return
        
        # Выбор и выполнение атаки
        self._execute_attack()

    def _handle_border_collision(self):
        """Обработка столкновений с границами экрана"""
        if self.rect.right > self.screen_width - 50:
            self.speed_x = -BOSS_SPEED_X
        if self.rect.left < 50:
            self.speed_x = BOSS_SPEED_X
        
        if self.rect.y > self.initial_y + 20:
            self.speed_y = -BOSS_SPEED_Y
        if self.rect.y < self.initial_y - 20:
            self.speed_y = BOSS_SPEED_Y

    def _execute_attack(self):
        """Выполнение случайной атаки с учетом задержки"""
        # Расчет задержки в зависимости от счета игрока
        current_cooldown = max(
            MIN_ATTACK_COOLDOWN,
            INITIAL_ATTACK_COOLDOWN - (self.player.score // 100) * 50
        )
        
        now = pygame.time.get_ticks()
        if now - self.last_attack > current_cooldown:
            self.last_attack = now
            random.choice(self.attack_types)()

    # Методы атак
    def single_shot_center(self):
        """Одиночный выстрел по центру"""
        self._create_bullet(self.rect.centerx, self.rect.bottom, 0, ENEMY_BULLET_SPEED)

    def single_shot_sides(self):
        """Двойной выстрел по бокам"""
        self._create_bullet(self.rect.left + 20, self.rect.bottom, 0, ENEMY_BULLET_SPEED)
        self._create_bullet(self.rect.right - 20, self.rect.bottom, 0, ENEMY_BULLET_SPEED)

    def single_shot_center_and_sides(self):
        """Тройной выстрел - центр и бока"""
        self._create_bullet(self.rect.centerx, self.rect.bottom, 0, ENEMY_BULLET_SPEED)
        self._create_bullet(self.rect.left + 20, self.rect.bottom, 0, ENEMY_BULLET_SPEED)
        self._create_bullet(self.rect.right - 20, self.rect.bottom, 0, ENEMY_BULLET_SPEED)

    def spread_shot(self):
        """Веерный выстрел под разными углами"""
        for i in range(-2, 3):
            angle = i * 15
            rad_angle = math.radians(angle)
            speed_x = math.sin(rad_angle) * ENEMY_BULLET_SPEED
            speed_y = math.cos(rad_angle) * ENEMY_BULLET_SPEED
            self._create_bullet(self.rect.centerx, self.rect.bottom, speed_x, speed_y)

    def exploding_bullet_shot(self):
        """Выстрел взрывающейся пулей"""
        bullet = ExplodingBullet(
            self.rect.centerx, 
            self.rect.bottom, 
            ENEMY_BULLET_SPEED, 
            self.all_sprites, 
            self.enemy_bullets
        )
        self.all_sprites.add(bullet)
        self.enemy_bullets.add(bullet)

    def rapid_fire_start(self):
        """Начало очереди быстрых выстрелов"""
        self.rapid_fire_state = BULLETS_PER_RAPID_FIRE
        self.rapid_fire_last_shot = pygame.time.get_ticks()

    def rapid_fire_state_machine(self):
        """Обработка очереди выстрелов"""
        now = pygame.time.get_ticks()
        if now - self.rapid_fire_last_shot > RAPID_FIRE_DELAY and self.rapid_fire_state > 0:
            self._create_bullet(self.rect.centerx, self.rect.bottom, 0, ENEMY_BULLET_SPEED)
            self.rapid_fire_state -= 1
            self.rapid_fire_last_shot = now
            
            if self.rapid_fire_state == 0:
                self.last_attack = now

    def _create_bullet(self, x, y, speed_x, speed_y):
        """Создание пули и добавление в группы"""
        bullet = EnemyBullet(x, y, speed_x, speed_y)
        self.all_sprites.add(bullet)
        self.enemy_bullets.add(bullet)