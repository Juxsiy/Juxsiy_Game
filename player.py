import pygame
from bullet import Bullet

PLAYER_SPEED = 5
LIVES = 3
SHOOT_COOLDOWN = 250

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.speed = PLAYER_SPEED
        self.lives = LIVES
        self.score = 0
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
        if self.rect.top < self.screen_height * 1 / 3:
            self.rect.top = self.screen_height * 1 / 3

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > SHOOT_COOLDOWN:
            self.last_shot = now
            new_bullet = Bullet(self.rect.centerx, self.rect.top)
            return new_bullet
        return None