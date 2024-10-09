import math
import pygame
import random

# Initialize Pygame.
pygame.init()

# Set the dimensions of the game window.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title and icon of the window.
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders-game-project/assets/images/spaceship.png")
icon = pygame.transform.scale(icon, (32, 32))  # Resize the icon
pygame.display.set_icon(icon)

# Player settings.
player_img = pygame.image.load("space-invaders-game-project/assets/images/player.png")
player_img = pygame.transform.scale(player_img, (64, 64))  # Adjust the player size.
player_x = 370  # Initial player position.
player_y = 480
player_x_change = 0  # Change in player position.

# Enemy settings.
enemy_img = pygame.image.load("space-invaders-game-project/assets/images/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 64))  # Adjust the enemy size.
enemy_x = random.randint(0, screen_width - 64)  # Random initial enemy position.
enemy_y = random.randint(50, 150)
enemy_x_change = 0.5  # Speed of the enemy.
enemy_y_change = 40   # Change in enemy's vertical position.

# Bullet settings.
bullet_img = pygame.image.load("space-invaders-game-project/assets/images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (32, 32))  # Adjust the bullet size.
bullet_x = 0  # Initial bullet position.
bullet_y = player_y  # Bullet starts from player's position.
bullet_y_change = 1.0  # Speed of the bullet.
bullet_state = "ready"  # "ready" = not visible; "fire" = bullet is moving.

# Score settings.
score = 0
font = pygame.font.Font(None, 36)  # Font for displaying the score.


# Function to display the score on the screen.
def show_score(x, y):
    score_display = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_display, (x, y))


# Function to draw the player on the screen.
def player(x, y):
    screen.blit(player_img, (x, y))


# Function to draw the enemy on the screen.
def enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Function to fire the bullet.
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Change the bullet state to "fire".
    screen.blit(bullet_img, (x + 16, y + 10))  # Draw the bullet.


# Function to check for collision between the bullet and the enemy.
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27  # Collision radius to detect hit.


# Function to check if the game is over.
def is_game_over(enemy_x, enemy_y):
    if enemy_y > player_y:  # Check if the enemy passes the player's position.
        return True
    if (enemy_x < player_x + 64 and enemy_x + 64 > player_x) and enemy_y + 64 > player_y:
        return True  # Check for collision with the side of the player.
    return False


# Function to display the game over message.
def game_over():
    font = pygame.font.Font(None, 64)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    
    # Center the text on the screen.
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, text_rect)
    
    pygame.display.update()  # Update the display.
    pygame.time.delay(3000)  # Delay to show the game over message.
    pygame.quit()  # Quit Pygame.

# Game loop.
running = True
while running:

    # Fill the screen with white color.
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Move left.
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:  # Move right.
                player_x_change = 0.3
            if event.key == pygame.K_UP:  # Fire bullet using the up arrow.
                if bullet_state == "ready":
                    bullet_x = player_x  # Set bullet's x position to the player's x.
                    fire_bullet(bullet_x, bullet_y)  # Fire the bullet.

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0  # Stop moving when the key is released.

    # Update the player's position.
    player_x += player_x_change
    if player_x <= 0:  # Boundary check for the left side.
        player_x = 0
    elif player_x >= screen_width - 64:  # Boundary check for the right side.
        player_x = screen_width - 64

    # Move the enemy.
    enemy_x += enemy_x_change
    if enemy_x <= 0:  # Enemy reaches the left boundary.
        enemy_x_change = 0.5  # Reverse direction.
        enemy_y += enemy_y_change  # Move down.
    elif enemy_x >= screen_width - 64:  # Enemy reaches the right boundary.
        enemy_x_change = -0.5  # Reverse direction.
        enemy_y += enemy_y_change  # Move down.

    # Check if the enemy reaches the bottom of the screen (game over).
    if is_game_over(enemy_x, enemy_y):
        game_over()
        running = False

    # Bullet movement.
    if bullet_y <= 0:  # If the bullet reaches the top of the screen.
        bullet_y = player_y  # Reset bullet position.
        bullet_state = "ready"  # Set bullet state to ready.
    if bullet_state == "fire":  # If the bullet is in the fire state.
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change  # Move the bullet upward.

    # Check for collision.
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:  # If a collision is detected.
        bullet_y = player_y  # Reset bullet position.
        bullet_state = "ready"  # Set bullet state to ready.
        enemy_x = random.randint(0, screen_width - 64)  # Spawn a new enemy.
        enemy_y = random.randint(50, 150)
        score += 1  # Increment score when the enemy is destroyed.

    # Draw the player, enemy, and score on the screen.
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(10, 10)  # Display the score in the top-left corner.

    # Update the display.
    pygame.display.update()
