import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Платформер")
clock = pygame.time.Clock()

# Загрузка изображений
player_image = pygame.image.load('RoboDog.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # Изменение размера робособаки
player = player_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))

plane_image = pygame.image.load('plane.png')
plane_image = pygame.transform.scale(plane_image, (200, 50))  # Изменение размера самолета
planes = [plane_image.get_rect(topleft=(0, HEIGHT - 70)),
          plane_image.get_rect(topleft=(WIDTH // 2 - 100, HEIGHT - 200)),
          plane_image.get_rect(topleft=(WIDTH // 4, HEIGHT - 350))]

# Переменные игрока
player_velocity = 0
gravity = 0.5
jump_strength = -10
on_ground = False
lives = 3
font = pygame.font.Font(None, 36)

# Переменные для препятствий
balls = []
ball_speed = 5
ball_spawn_rate = 30  # Каждые 30 кадров

# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity = jump_strength
        on_ground = False

    # Применение гравитации
    player_velocity += gravity
    player.y += player_velocity

    # Обработка столкновений с самолетами
    on_ground = False
    for plane in planes:
        if player.colliderect(plane) and player_velocity > 0:
            player.y = plane.y - player.height
            player_velocity = 0
            on_ground = True

    # Ограничение движений игрока по границам экрана
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width
    if player.y > HEIGHT:
        player.y = HEIGHT - player.height
        player_velocity = 0
        on_ground = True

    # Спавн черных шаров (препятствий)
    if random.randint(1, ball_spawn_rate) == 1:
        ball = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)
        balls.append(ball)

    # Движение черных шаров
    for ball in balls[:]:
        ball.y += ball_speed
        if ball.colliderect(player):
            balls.remove(ball)
            lives -= 1
            if lives <= 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()
        elif ball.y > HEIGHT:
            balls.remove(ball)

    # Отрисовка
    screen.fill(WHITE)
    screen.blit(player_image, player.topleft)
    for plane in planes:
        screen.blit(plane_image, plane.topleft)

    # Отрисовка черных шаров
    for ball in balls:
        pygame.draw.ellipse(screen, BLACK, ball)

    # Отображение жизней
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(FPS)
