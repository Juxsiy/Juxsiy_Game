import pygame

# Константы
ENEMY_BULLET_SPEED = 7
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 0, 0)  # Красный

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        
        # Создание изображения
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        
        # Позиционирование пули
        self.rect.centerx = x
        self.rect.top = y
        
        # Скорости движения
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        """Обновление позиции пули"""
        # Движение пули по вектору
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Получение размеров экрана
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        
        # Удаление пули при выходе за границы экрана
        if (self.rect.top > screen_height or
            self.rect.bottom < 0 or
            self.rect.right < 0 or
            self.rect.left > screen_width):
            self.kill()