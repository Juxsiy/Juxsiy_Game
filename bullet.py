import pygame

# Константы
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 255, 0)  # Желтый

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Создание изображения
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        
        # Позиционирование пули
        self.rect.centerx = x
        self.rect.bottom = y
        
        # Скорость движения (минус - движение вверх)
        self.speed = -BULLET_SPEED

    def update(self):
        """Обновление позиции пули"""
        # Движение пули вверх
        self.rect.y += self.speed
        
        # Удаление пули при выходе за верхнюю границу
        if self.rect.bottom < 0:
            self.kill()