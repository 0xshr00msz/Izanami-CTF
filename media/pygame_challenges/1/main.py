"""
Izanami CTF - Memory Manipulation Challenge
A simple Pygame game where the player needs to find and manipulate memory values to reveal the flag.
"""

import pygame
import sys
import random
import time
import asyncio

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game variables
score = 0
level = 1
health = 100
chakra = 50
secret_counter = 0
hidden_values = [42, 13, 37, 73]
collected_values = []
flag_parts = ["izanami{", "m3m0ry_", "m4n1pul4t10n_", "m4st3r}"]
flag_revealed = [False, False, False, False]

# Create the game window
screen = pygame.Surface((WIDTH, HEIGHT))
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Izanami Memory Challenge")

# Load fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)

# Game objects
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5
        self.size = 20
        self.color = RED
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size))
    
    def move(self, dx, dy):
        self.x = max(self.size // 2, min(WIDTH - self.size // 2, self.x + dx))
        self.y = max(self.size // 2, min(HEIGHT - self.size // 2, self.y + dy))

class Collectible:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)
        self.size = 15
        self.color = GREEN
        self.value = random.choice(hidden_values)
        self.collected = False
    
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
    
    def check_collision(self, player):
        if not self.collected:
            distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
            if distance < (player.size // 2 + self.size):
                self.collected = True
                return True
        return False

class Enemy:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)
        self.speed = random.uniform(1, 3)
        self.size = 25
        self.color = BLUE
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
    
    def move(self, player):
        # Move towards the player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.x += dx / distance * self.speed
        self.y += dy / distance * self.speed
    
    def check_collision(self, player):
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        return distance < (player.size // 2 + self.size)

# Create game objects
player = Player()
collectibles = [Collectible() for _ in range(5)]
enemies = [Enemy() for _ in range(3)]

# Game state
game_over = False
game_won = False

# Hidden functions that can be discovered through memory manipulation
def _check_secret_values():
    global collected_values, flag_revealed
    
    # Check for specific patterns in collected values
    if 42 in collected_values and not flag_revealed[0]:
        flag_revealed[0] = True
        print("You found the first part of the flag!")
        print(f"FLAG PART 1: {flag_parts[0]}")
    
    if 13 in collected_values and 37 in collected_values and not flag_revealed[1]:
        flag_revealed[1] = True
        print("You found the second part of the flag!")
        print(f"FLAG PART 2: {flag_parts[1]}")
    
    if collected_values.count(73) >= 2 and not flag_revealed[2]:
        flag_revealed[2] = True
        print("You found the third part of the flag!")
        print(f"FLAG PART 3: {flag_parts[2]}")
    
    # Check if all values have been collected in the right order
    if all(flag_revealed[:3]) and secret_counter >= 10 and not flag_revealed[3]:
        flag_revealed[3] = True
        print("You found the final part of the flag!")
        print(f"FLAG PART 4: {flag_parts[3]}")
        
    # Check if all flag parts have been revealed
    if all(flag_revealed):
        print(f"FLAG: {''.join(flag_parts)}")

def _increment_secret_counter():
    global secret_counter
    secret_counter += 1
    if secret_counter % 5 == 0:
        print(f"Secret counter: {secret_counter}")

# Main game loop
async def main():
    global score, health, chakra, game_over, game_won, collected_values
    
    clock = pygame.time.Clock()
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Secret key combination to reveal a hint
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    print("HINT: Look for patterns in the memory values. Try to collect specific values.")
                if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    print("MEMORY VALUES:", hidden_values)
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    print("COLLECTED VALUES:", collected_values)
        
        if not game_over and not game_won:
            # Get keyboard input
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = player.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = player.speed
            
            # Move player
            player.move(dx, dy)
            
            # Move enemies
            for enemy in enemies:
                enemy.move(player)
                if enemy.check_collision(player):
                    health -= 1
                    if health <= 0:
                        game_over = True
            
            # Check collectibles
            for collectible in collectibles:
                if collectible.check_collision(player):
                    score += 10
                    chakra += 5
                    collected_values.append(collectible.value)
                    _check_secret_values()
                    collectibles.remove(collectible)
                    collectibles.append(Collectible())
            
            # Increment secret counter
            _increment_secret_counter()
            
            # Check win condition
            if all(flag_revealed):
                game_won = True
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw game objects
        for collectible in collectibles:
            collectible.draw()
        
        for enemy in enemies:
            enemy.draw()
        
        player.draw()
        
        # Draw UI
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        health_text = font_small.render(f"Health: {health}", True, WHITE)
        chakra_text = font_small.render(f"Chakra: {chakra}", True, WHITE)
        level_text = font_small.render(f"Level: {level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(chakra_text, (10, 70))
        screen.blit(level_text, (10, 100))
        
        # Draw flag parts that have been revealed
        flag_text = "Flag: "
        for i, revealed in enumerate(flag_revealed):
            if revealed:
                flag_text += flag_parts[i]
            else:
                flag_text += "????"
        
        flag_display = font_small.render(flag_text, True, WHITE)
        screen.blit(flag_display, (WIDTH - 350, 10))
        
        # Draw game over or win message
        if game_over:
            game_over_text = font_large.render("GAME OVER", True, RED)
            restart_text = font_medium.render("Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
            
            # Check for restart
            if pygame.key.get_pressed()[pygame.K_r]:
                # Reset game
                player = Player()
                collectibles = [Collectible() for _ in range(5)]
                enemies = [Enemy() for _ in range(3)]
                score = 0
                health = 100
                chakra = 50
                game_over = False
        
        if game_won:
            win_text = font_large.render("YOU WIN!", True, GREEN)
            flag_text = font_medium.render(f"Flag: {''.join(flag_parts)}", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(flag_text, (WIDTH // 2 - flag_text.get_width() // 2, HEIGHT // 2 + 20))
        
        # Update the display
        canvas.blit(screen, (0, 0))
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
        
        # Allow other tasks to run
        await asyncio.sleep(0)

# Run the game
asyncio.run(main())
