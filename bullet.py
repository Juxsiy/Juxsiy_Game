import pygame

# Константы
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 15

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()

        # Позиция снаряда
        self.rect.centerx = x
        self.rect.bottom = y

        # Скорость
        self.speed = -BULLET_SPEED # Отрицательное значение, чтобы снаряд летел вверх

    def update(self):
        # Двигаем снаряд вверх
        self.rect.y += self.speed

        # Удаляем снаряд, если он ушел за верхнюю границу экрана
        if self.rect.bottom < 0:
            self.kill()