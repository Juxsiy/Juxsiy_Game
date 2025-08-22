import pygame
import sys
from player import Player
from boss import Boss
from enemy_bullet import EnemyBullet
from exploding_bullet import ExplodingBullet
from database import DatabaseManager

# Инициализация PyGame
pygame.init()

# Получение информации о мониторе
display_info = pygame.display.Info()
MONITOR_WIDTH = display_info.current_w
MONITOR_HEIGHT = display_info.current_h

# Расчет размеров игрового окна
SCREEN_HEIGHT = int(MONITOR_HEIGHT * 0.9)
SCREEN_WIDTH = int(SCREEN_HEIGHT * 0.75)

if SCREEN_WIDTH > MONITOR_WIDTH:
    SCREEN_WIDTH = int(MONITOR_WIDTH * 0.9)
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 1.33)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space War")

FPS = 60
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)

# Глобальные группы спрайтов
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

def draw_text_centered(text, font_size, color, y_offset):
    """Рисует текст по центру экрана"""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
    screen.blit(text_surface, text_rect)
    return text_rect

def draw_multiline_text(lines, font_size, color, start_y, line_spacing):
    """Рисует несколько строк текста"""
    for i, line in enumerate(lines):
        draw_text_centered(line, font_size, color, start_y + i * line_spacing)

def get_player_name():
    """Функция для ввода имени игрока"""
    player_name = ""
    input_active = True
    
    instructions = [
        "Управление: Стрелки или WASD",
        "Цель игры: Выжить 60 секунд под атаками босса!",
        "Нажмите Enter, чтобы начать"
    ]

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        
        screen.fill(BLACK)
        
        # Заголовок
        draw_text_centered("Введите ваше имя:", int(SCREEN_HEIGHT * 0.05), WHITE, 
                          SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 0.05)
        
        # Инструкции
        draw_multiline_text(instructions, int(SCREEN_HEIGHT * 0.03), BLUE,
                           SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 0.2, 
                           int(SCREEN_HEIGHT * 0.04))
        
        # Поле ввода
        if player_name:
            draw_text_centered(player_name, int(SCREEN_HEIGHT * 0.05), WHITE,
                              SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 0.03)

        
        pygame.display.flip()
        clock.tick(30)
        
    return player_name

def show_end_screen(player_name, score, status):
    """Отображает экран окончания игры и таблицу рекордов"""
    db = DatabaseManager()
    db.save_score(player_name, score)
    top_scores = db.get_top_scores()

    # Создаем кнопку
    button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))
    button_text = button_font.render("Начать заново", True, WHITE)
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.75))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                waiting = False
                    
        screen.fill(BLACK)
        
        # Статус игры
        draw_text_centered("Вы выиграли!" if status == 'win' else "Game Over", 
                          int(SCREEN_HEIGHT * 0.09), 
                          GREEN if status == 'win' else RED,
                          SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 0.2)
        
        # Счет игрока
        draw_text_centered(f"Ваш счет: {score}", 
                          int(SCREEN_HEIGHT * 0.06), WHITE,
                          SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 0.13)
        
        # Таблица рекордов
        draw_text_centered("Топ-5 игроков:", 
                          int(SCREEN_HEIGHT * 0.045), WHITE,
                          SCREEN_HEIGHT // 2)
        
        # Отображение топ-5 результатов
        for i, (name, score_val) in enumerate(top_scores):
            draw_text_centered(f"{i + 1}. {name}: {score_val}", 
                              int(SCREEN_HEIGHT * 0.04), WHITE,
                              SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 0.05 + i * SCREEN_HEIGHT * 0.035)

        # Кнопка
        pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))
        
        pygame.display.flip()

def main_game_loop(player_name):
    """Основной игровой цикл"""
    # Очистка групп спрайтов
    all_sprites.empty()
    player_bullets.empty()
    enemy_bullets.empty()
    enemies.empty()

    # Создание игрока и босса
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    boss = Boss(SCREEN_WIDTH, all_sprites, enemy_bullets, player)
    
    all_sprites.add(player)
    enemies.add(boss)

    game_state = 'playing'
    start_time = pygame.time.get_ticks()
    WIN_TIME = 60000  # 60 секунд

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == 'playing':
            # Проверка времени победы
            if pygame.time.get_ticks() - start_time > WIN_TIME:
                game_state = 'win'
                
            # Обновление спрайтов
            all_sprites.update()
            enemies.update()
            
            # Стрельба игрока
            new_bullet = player.shoot()
            if new_bullet:
                all_sprites.add(new_bullet)
                player_bullets.add(new_bullet)

            # Проверка столкновений
            hits = pygame.sprite.groupcollide(player_bullets, enemies, True, False)
            for hit in hits:
                player.score += 10
            
            # Проверка попадания в игрока
            player_hit = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if player_hit:
                player.lives -= 1
                if player.lives <= 0:
                    game_state = 'loss'
        
        # Отрисовка
        screen.fill(BLACK)
        all_sprites.draw(screen)
        enemies.draw(screen)
        enemy_bullets.draw(screen)
        
        # Отображение HUD
        font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.045))
        score_text = font.render(f"Счет: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f"Жизни: {player.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        # Проверка состояния игры
        if game_state in ('win', 'loss'):
            show_end_screen(player_name, player.score, game_state)
            return

        pygame.display.flip()

if __name__ == '__main__':
    while True:
        player_name = get_player_name()
        main_game_loop(player_name)