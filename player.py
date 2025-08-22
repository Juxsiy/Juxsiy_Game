import pygame
from bullet import Bullet

# Константы
PLAYER_SPEED = 7
LIVES = 3
SHOOT_COOLDOWN = 150  # мс между выстрелами

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        
        # Создание изображения
        self.image = pygame.image.load('player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20
        
        # Параметры экрана
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Игровые параметры
        self.speed = PLAYER_SPEED
        self.lives = LIVES
        self.score = 0
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        """Обновление позиции игрока"""
        keys = pygame.key.get_pressed()
        
        # Движение
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # Ограничение движения в пределах экрана
        self.rect.right = min(self.rect.right, self.screen_width)
        self.rect.left = max(self.rect.left, 0)
        self.rect.bottom = min(self.rect.bottom, self.screen_height)
        self.rect.top = max(self.rect.top, self.screen_height // 3)

    def shoot(self):
        """Создание пули при стрельбе"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > SHOOT_COOLDOWN:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None