import pygame
import random
import time

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎯 Aim Trainer")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 24)

# Game variables
score = 0
misses = 0
target_radius = 30
target_pos = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))

start_time = time.time()
game_duration = 30  # seconds

# Reaction time
last_click_time = time.time()
reaction_times = []

running = True

while running:
    screen.fill(WHITE)

    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, int(game_duration - elapsed_time))

    # Draw target
    pygame.draw.circle(screen, RED, target_pos, target_radius)

    # Draw text
    score_text = font.render(f"Score: {score}", True, BLACK)
    time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    miss_text = font.render(f"Misses: {misses}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 40))
    screen.blit(miss_text, (10, 70))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            distance = ((mouse_pos[0] - target_pos[0])**2 + (mouse_pos[1] - target_pos[1])**2)**0.5

            if distance <= target_radius:
                score += 1

                # Reaction time
                click_time = time.time()
                reaction_times.append(click_time - last_click_time)
                last_click_time = click_time

                # New target
                target_pos = (
                    random.randint(50, WIDTH-50),
                    random.randint(50, HEIGHT-50)
                )
            else:
                misses += 1

    # End game
    if elapsed_time >= game_duration:
        running = False

    pygame.display.update()

# Game Over Screen
screen.fill(WHITE)

avg_reaction = sum(reaction_times)/len(reaction_times) if reaction_times else 0

game_over_text = font.render("Game Over!", True, BLACK)
score_text = font.render(f"Final Score: {score}", True, BLACK)
miss_text = font.render(f"Misses: {misses}", True, BLACK)
reaction_text = font.render(f"Avg Reaction: {round(avg_reaction, 3)} sec", True, BLACK)

screen.blit(game_over_text, (WIDTH//2 - 60, HEIGHT//2 - 60))
screen.blit(score_text, (WIDTH//2 - 80, HEIGHT//2 - 20))
screen.blit(miss_text, (WIDTH//2 - 80, HEIGHT//2 + 10))
screen.blit(reaction_text, (WIDTH//2 - 100, HEIGHT//2 + 40))

pygame.display.update()

# Wait before closing
pygame.time.delay(5000)

pygame.quit()