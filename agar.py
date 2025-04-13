import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agar.io Clone")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player class
class Cell:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed
            self.y += dx * self.speed

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.hypot(dx, dy)
        return dist < self.radius + other.radius

# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 5
        self.color = GREEN

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Game setup
player = Cell(WIDTH // 2, HEIGHT // 2, 20, RED, 5)
foods = [Food() for _ in range(50)]
enemies = [Cell(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(10, 30), BLUE, 3) for _ in range(10)]
score = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player towards mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.move(mouse_x, mouse_y)

    # Check collisions with food
    for food in foods[:]:
        if player.collide(food):
            foods.remove(food)
            player.radius += 1
            score += 1
            foods.append(Food())  # Respawn food

    # Check collisions with enemies
    for enemy in enemies[:]:
        # Random movement for enemies
        target_x = enemy.x + random.randint(-50, 50)
        target_y = enemy.y + random.randint(-50, 50)
        enemy.move(target_x, target_y)

        if player.collide(enemy):
            if player.radius > enemy.radius:
                player.radius += enemy.radius // 2
                score += enemy.radius
                enemies.remove(enemy)
                enemies.append(Cell(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(10, 30), BLUE, 3))
            elif player.radius < enemy.radius:
                running = False  # Game over

    # Draw everything
    screen.fill(WHITE)
    for food in foods:
        food.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()