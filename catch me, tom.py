import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load the background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load the cheese image
cheese_size = 50
cheese_image = pygame.image.load("cheese-1.png")  # Replace "cheese-1.png" with your image file name
cheese_image = pygame.transform.scale(cheese_image, (cheese_size, cheese_size))  # Scale to fit the cheese size

# Load the mouse image
mouse_size = 80
mouse_image_r1 = pygame.transform.scale(pygame.image.load("mouse-R1.png"), (mouse_size, mouse_size))
mouse_image_l1 = pygame.transform.scale(pygame.image.load("mouse-L1.png"), (mouse_size, mouse_size))

# Load the cat image
cat_size = 80
cat_image_r1 = pygame.transform.scale(pygame.image.load("cat-R1.png"), (cat_size, cat_size))
cat_image_l1 = pygame.transform.scale(pygame.image.load("cat-L1.png"), (cat_size, cat_size))

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for buttons and text
font = pygame.font.Font(None, 50)

# Mouse attributes
mouse_size = 80
mouse_x = WIDTH // 2
mouse_y = HEIGHT - mouse_size
mouse_speed = 8

# Cheese attributes
cheese_size = 50
cheese_x = random.randint(0, WIDTH - cheese_size)
cheese_y = random.randint(0, HEIGHT - cheese_size)

# Cat attributes
cat_size = 80
cat_x = random.randint(0, WIDTH - cat_size)
cat_y = random.randint(0, HEIGHT - cat_size)
cat_speed = 2.5

# Walls configuration for each round
walls_rounds = [
    [],  # Round 1: No walls
    [
        pygame.Rect(300, 0, 20, 300),  # Left vertical wall
        pygame.Rect(500, 300, 20, 300) # Right vertical wall
    ],  # Round 2: Two walls
    [
        pygame.Rect(200, 0, 20, 400),
        pygame.Rect(400, 100, 20, 400),
        pygame.Rect(600, 200, 20, 400)
    ]  # Round 3: Three walls
]

# Score and round
score = 0
round_number = 1

# Background Music
pygame.mixer.music.load("background_music.mp3")  # Replace with your music file
pygame.mixer.music.set_volume(0.5)  # Set the volume (range 0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop the music indefinitely

def reset_positions():
    global mouse_x, mouse_y, cat_x, cat_y, cheese_x, cheese_y
    mouse_x, mouse_y = WIDTH // 2, HEIGHT - mouse_size
    cat_x, cat_y = random.randint(0, WIDTH - cat_size), random.randint(0, HEIGHT - cat_size)
    cheese_x, cheese_y = random.randint(0, WIDTH - cheese_size), random.randint(0, HEIGHT - cheese_size)

# Home screen function
def show_home_screen():
    while True:
        # Drawing everything
        screen.blit(background_image, (0, 0))

        # Draw title
        title_text = font.render("Welcome to the Game!", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw buttons
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, BLUE, start_button)
        pygame.draw.rect(screen, RED, quit_button)

        start_text = font.render("Start", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 10))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    return  # Start the game
                if quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()

def show_result_screen(result):
    while True:
        # Drawing everything
        screen.blit(background_image, (0, 0))

        # Display result message
        result_text = font.render(f"YOU {result}!", True, BLACK)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 4))

        # Draw Back to Home button
        home_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
        pygame.draw.rect(screen, BLUE, home_button)

        home_text = font.render("Back to Home", True, WHITE)
        screen.blit(home_text, (home_button.x + (home_button.width - home_text.get_width()) // 2, home_button.y + 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if home_button.collidepoint(mouse_x, mouse_y):
                    return  # Return to home screen

def game_loop():
    global mouse_x, mouse_y, cat_x, cat_y, cheese_x, cheese_y, score, round_number
    running = True
    target_scores = [5, 5, 10]  # Scores required for each round

    while running:
        # Set current walls based on the round
        walls = walls_rounds[round_number - 1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and mouse_x > 0:
            mouse_x -= mouse_speed
        if keys[pygame.K_RIGHT] and mouse_x < WIDTH - mouse_size:
            mouse_x += mouse_speed
        if keys[pygame.K_UP] and mouse_y > 0:
            mouse_y -= mouse_speed
        if keys[pygame.K_DOWN] and mouse_y < HEIGHT - mouse_size:
            mouse_y += mouse_speed

        # Check for collisions with walls
        for wall in walls:
            if wall.colliderect(mouse_x, mouse_y, mouse_size, mouse_size):
                if mouse_x < wall.left:  # Collision from the left
                    mouse_x = wall.left - mouse_size
                elif mouse_x + mouse_size > wall.right:  # Collision from the right
                    mouse_x = wall.right

        # Move cat towards mouse
        dx = mouse_x - cat_x
        dy = mouse_y - cat_y
        distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)  # Avoid division by zero
        cat_x += cat_speed * (dx / distance)
        cat_y += cat_speed * (dy / distance)

        # Check for cat collisions with walls
        for wall in walls:
            if wall.colliderect(cat_x, cat_y, cat_size, cat_size):
                if cat_x < wall.left:  # Collision from the left
                    cat_x = wall.left - cat_size
                elif cat_x + cat_size > wall.right:  # Collision from the right
                    cat_x = wall.right
                if cat_y < wall.top:  # Collision from the top
                    cat_y = wall.top - cat_size
                elif cat_y + cat_size > wall.bottom:  # Collision from the bottom
                    cat_y = wall.bottom

        # Check collision with cheese
        if (mouse_x < cheese_x + cheese_size and mouse_x + mouse_size > cheese_x and
            mouse_y < cheese_y + cheese_size and mouse_y + mouse_size > cheese_y):
            score += 1
            cheese_x = random.randint(0, WIDTH - cheese_size)
            cheese_y = random.randint(0, HEIGHT - cheese_size)

        # Check collision with cat
        if (mouse_x < cat_x + cat_size and mouse_x + mouse_size > cat_x and
            mouse_y < cat_y + cat_size and mouse_y + mouse_size > cat_y):
            show_result_screen("LOSE")
            return

        # Check if round is complete
        if score >= target_scores[round_number - 1]:
            if round_number < 3:
                round_number += 1
                score = 0
                reset_positions()
                print(f"Round {round_number}!")
            else:
                show_result_screen("WIN")
                return

        # Drawing everything
        screen.blit(background_image, (0, 0))

        screen.blit(mouse_image_r1, (mouse_x, mouse_y))
        screen.blit(cheese_image, (cheese_x, cheese_y))
        screen.blit(cat_image_r1, (cat_x, cat_y))

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)

        # Display score and round
        score_text = font.render(f"Score: {score}", True, WHITE)
        round_text = font.render(f"Round: {round_number}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(round_text, (10, 50))

        # Update display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

# Show the home screen first
show_home_screen()

# Start the game loop
game_loop()

pygame.quit()
