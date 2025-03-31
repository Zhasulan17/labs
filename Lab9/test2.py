import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Background music
pygame.mixer.music.load('Кайрат Нуртас - Ауырмайды Жүрек.mp3')
pygame.mixer.music.play(-1)

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Disappearing Foods")
clock = pygame.time.Clock()

# Fonts and colors
font = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
speed = 15

# Food settings
food_spawn = True
food_timer = 0  # Timer for food to disappear
FOOD_LIFESPAN = 5000  # Milliseconds

# Create the first food
food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
food_weight = random.choice([1, 2, 3])
food_spawn_time = pygame.time.get_ticks()

# Score and level
game_score = 0
level = 1
threshold = 5  # Level up every 5 points

# Game loop flag
isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"

    # Update direction
    snake_direction = change_to

    # Move snake
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10

    # Insert new head
    snake_body.insert(0, list(snake_pos))

    # Check for food collision
    if snake_pos == food_pos:
        
        game_score += food_weight
        if game_score % threshold == 0:
            level += 1
            speed += 2
        food_spawn = False
    else:
        snake_body.pop()

    # Respawn new food if eaten or expired
    if not food_spawn or pygame.time.get_ticks() - food_spawn_time > FOOD_LIFESPAN:
        while True:
            new_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
            if new_pos not in snake_body:
                food_pos = new_pos
                food_weight = random.choice([1, 2, 3])
                food_spawn_time = pygame.time.get_ticks()
                food_spawn = True
                break

    # Wall collision
    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        isRunning = False

    # Self collision
    for block in snake_body[1:]:
        if snake_pos == block:
            isRunning = False

    # Drawing
    screen.fill(BLACK)
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))
    
    # Draw food with color based on weight
    if food_weight == 1:
        food_color = RED
    elif food_weight == 2:
        food_color = (255, 165, 0)  # Orange
    else:
        food_color = (255, 255, 0)  # Yellow

    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Draw text
    game_score_text = font.render(f"Score: {game_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    food_timer_text = font.render(
        f"Food disappears in: {max(0, (FOOD_LIFESPAN - (pygame.time.get_ticks() - food_spawn_time)) // 1000)}s",
        True, WHITE)

    screen.blit(game_score_text, (20, 20))
    screen.blit(level_text, (20, 50))
    screen.blit(food_timer_text, (20, 80))

    pygame.display.update()
    clock.tick(speed)

# Game Over screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(6500)
pygame.quit()
