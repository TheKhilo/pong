import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Pong")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
paddle_speed = 10

# Ball settings
BALL_SIZE = 20
ball_speed_x = 5
ball_speed_y = 5

# Paddle positions
paddle1_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
paddle2_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2

# Ball position
ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2

# Score tracking
score1 = 0
score2 = 0

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Power-up settings
power_up_active = False
power_up_type = None
power_up_timer = 0
power_up_x = random.randint(100, SCREEN_WIDTH - 100)
power_up_y = random.randint(100, SCREEN_HEIGHT - 100)

def draw_background():
    for y in range(0, SCREEN_HEIGHT, 2):
        color = (0, int(255 * (y / SCREEN_HEIGHT)), int(255 * (y / SCREEN_HEIGHT)))
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def draw_particles():
    for _ in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, YELLOW, (x, y), 2)

def draw_power_up():
    if power_up_active:
        pygame.draw.circle(screen, RED if power_up_type == 'speed' else BLUE, (power_up_x, power_up_y), 15)

def activate_power_up():
    global ball_speed_x, ball_speed_y, paddle_speed, power_up_active, power_up_type
    if power_up_type == 'speed':
        ball_speed_x *= 1.5
        ball_speed_y *= 1.5
    elif power_up_type == 'slow':
        ball_speed_x *= 0.5
        ball_speed_y *= 0.5
    power_up_active = False

# Game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)  # Clear the screen each frame

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle1_y += paddle_speed
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle2_y += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top/bottom
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (ball_x <= PADDLE_WIDTH and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT) or \
       (ball_x >= SCREEN_WIDTH - PADDLE_WIDTH - BALL_SIZE and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    # Ball reset if it goes out of bounds
    if ball_x < 0:
        score2 += 1
        ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
        ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
        ball_speed_x = 5 * random.choice([-1, 1])
        ball_speed_y = 5 * random.choice([-1, 1])

    if ball_x > SCREEN_WIDTH:
        score1 += 1
        ball_x = (SCREEN_WIDTH - BALL_SIZE) // 2
        ball_y = (SCREEN_HEIGHT - BALL_SIZE) // 2
        ball_speed_x = 5 * random.choice([-1, 1])
        ball_speed_y = 5 * random.choice([-1, 1])

    # Power-up appearance
    if not power_up_active and random.randint(0, 1000) < 5:
        power_up_active = True
        power_up_type = random.choice(['speed', 'slow'])
        power_up_x = random.randint(100, SCREEN_WIDTH - 100)
        power_up_y = random.randint(100, SCREEN_HEIGHT - 100)

    # Power-up collision
    if power_up_active and ball_x in range(power_up_x - 15, power_up_x + 15) and ball_y in range(power_up_y - 15, power_up_y + 15):
        activate_power_up()
        power_up_timer = pygame.time.get_ticks()

    # Deactivate power-up after some time
    if power_up_timer and pygame.time.get_ticks() - power_up_timer > 5000:
        ball_speed_x = 5 * (1 if ball_speed_x > 0 else -1)
        ball_speed_y = 5 * (1 if ball_speed_y > 0 else -1)
        power_up_timer = 0

    # Drawing everything
    draw_background()
    draw_particles()
    pygame.draw.rect(screen, RED, (0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, GREEN, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    draw_power_up()

    # Display scores
    text1 = font.render(str(score1), True, WHITE)
    screen.blit(text1, (SCREEN_WIDTH // 4, 10))
    text2 = font.render(str(score2), True, WHITE)
    screen.blit(text2, (3 * SCREEN_WIDTH // 4, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
