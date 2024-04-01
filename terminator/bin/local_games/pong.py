import random
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


print('\n1')
time.sleep(1)
print('\n2')
time.sleep(1)
print('\n3')
time.sleep(1)
print('\nGO!!')

# Initialize PyGame
pygame.init()

# Set the window size
window_size = (1000, 700)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption('PONG')

# Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 20, 100)

# Set the font
font = pygame.font.Font(None, 48)

# Set the players' scores to 0
player_1_score = 0
player_2_score = 0

# Set the player 1 paddle variables
player_1_x = 70
player_1_y = 250
player_1_width = 30
player_1_height = 120

# Set the player 2 paddle variables
player_2_x = 890
player_2_y = 250
player_2_width = 30
player_2_height = 120

# Set the ball variables
ball_x = 400
ball_y = 400
ball_radius = 30
ball_dx = random.choice([-1, 1])
ball_dy = random.choice([-1, 1])

# Set the game over flag to False
game_over = False

# Run the game loop
while not game_over:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

    # Check for player 1 input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_1_y >= 0:
        player_1_y -= 2
    if keys[pygame.K_s] and player_1_y <= window_size[1] - player_1_height:
        player_1_y += 2

    # Check for player 2 input
    if keys[pygame.K_UP] and player_2_y >= 0:
        player_2_y -= 2
    if keys[pygame.K_DOWN] and player_2_y <= window_size[1] - player_2_height:
        player_2_y += 2

    # Check for ball collision with top and bottom of window
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= window_size[1]:
        ball_dy *= -1

    # Check for ball collision with player 1 paddle
    if ball_x - ball_radius <= player_1_x + player_1_width and ball_y + ball_radius >= player_1_y \
            and ball_y - ball_radius <= player_1_y + player_1_height:
        ball_dx *= -1

    # Check for ball collision with player 2 paddle
    if ball_x + ball_radius >= player_2_x and ball_y + ball_radius >= player_2_y \
            and ball_y - ball_radius <= player_2_y + player_2_height:
        ball_dx *= -1

    # Check for ball going out of bounds on player 1's side
    if ball_x - ball_radius < 0:
        player_2_score += 1
        ball_x = 500
        ball_y = 500
        ball_dx = random.choice([-1, 1])
        ball_dy = random.choice([-1, 1])

    # Check for ball going out of bounds on player 2's side
    if ball_x + ball_radius > window_size[0]:
        player_1_score += 1
        ball_x = 500
        ball_y = 500
        ball_dx = random.choice([-1, 1])
        ball_dy = random.choice([-1, 1])

    # Update the ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Clear the screen
    screen.fill(black)

    # Draw the paddles
    pygame.draw.rect(screen, white, (player_1_x, player_1_y, player_1_width, player_1_height))
    pygame.draw.rect(screen, white, (player_2_x, player_2_y, player_2_width, player_2_height))

    # Draw the ball
    pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)

    # Draw the scores
    if player_1_score < 6:
        if player_2_score < 6:
            player_1_text = font.render(f'Player One: {player_1_score}', True, white)
            player_2_text = font.render(f'Player Two: {player_2_score}', True, white)
            screen.blit(player_1_text, (50, 50))
            screen.blit(player_2_text, (700, 50))
        else:
            player_1_text = font.render(f'Player One: LOST', True, white)
            player_2_text = font.render(f'Player Two: WON', True, white)
            screen.blit(player_1_text, (50, 50))
            screen.blit(player_2_text, (700, 50))
    else:
        player_1_text = font.render(f'Player One: WON', True, white)
        player_2_text = font.render(f'Player Two: LOST', True, white)
        screen.blit(player_1_text, (50, 50))
        screen.blit(player_2_text, (700, 50))

    # Update the display
    pygame.display.update()

# Quit PyGame
pygame.quit()
