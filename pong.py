import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the game window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game with Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
LIGHT_GRAY = (200, 200, 200)

# Define paddle and ball dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 15

# Define the speed for ball and paddles
BALL_SPEED_X, BALL_SPEED_Y = 7 * random.choice((1, -1)), 7 * random.choice((1, -1))
PADDLE_SPEED = 7

# Define game objects
player1_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

# Initialize scores
player1_score = 0
player2_score = 0

# Set up font
font = pygame.font.Font(None, 36)

# Function to display scores
def display_score():
    player1_text = font.render(f"{player1_score}", True, WHITE)
    player2_text = font.render(f"{player2_score}", True, WHITE)
    screen.blit(player1_text, (WIDTH // 2 - 60, 20))
    screen.blit(player2_text, (WIDTH // 2 + 20, 20))

# Function to handle ball movement and bouncing
def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, player1_score, player2_score

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top or bottom wall
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Ball collision with player paddles
    if ball.colliderect(player1_paddle) and BALL_SPEED_X < 0:
        BALL_SPEED_X *= -1
    if ball.colliderect(player2_paddle) and BALL_SPEED_X > 0:
        BALL_SPEED_X *= -1

    # Ball goes out of bounds (right side)
    if ball.right >= WIDTH:
        player1_score += 1
        reset_ball()

    # Ball goes out of bounds (left side)
    if ball.left <= 0:
        player2_score += 1
        reset_ball()

# Reset ball position to center
def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= random.choice((1, -1))
    BALL_SPEED_Y *= random.choice((1, -1))

# Handle player 1 (WASD) paddle movement
def move_player1():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.top -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
        player1_paddle.bottom += PADDLE_SPEED

# Handle player 2 (Arrow keys) paddle movement
def move_player2():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.top -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
        player2_paddle.bottom += PADDLE_SPEED

# Function to display the start menu with a slider to choose the win points
def show_menu():
    slider_value = 5
    running = True
    while running:
        screen.fill(BLACK)
        
        # Draw text
        title_text = font.render("Pong Game - Choose Win Points", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw slider
        pygame.draw.rect(screen, LIGHT_GRAY, (200, 300, 400, 10))
        pygame.draw.circle(screen, WHITE, (200 + int((slider_value - 1) * 400 / 19), 305), 15)

        # Draw slider value
        slider_text = font.render(f"Points to Win: {slider_value}", True, WHITE)
        screen.blit(slider_text, (WIDTH // 2 - slider_text.get_width() // 2, HEIGHT // 2 + 50))

        # Draw instructions to start
        start_text = font.render("Press ENTER to start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return slider_value
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, _ = pygame.mouse.get_pos()
                    if 200 <= mouse_x <= 600:
                        slider_value = int(1 + 19 * (mouse_x - 200) / 400)

        pygame.display.flip()

# Main game loop
def game_loop(points_to_win):
    global player1_score, player2_score

    player1_score = 0
    player2_score = 0
    clock = pygame.time.Clock()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game mechanics
        move_ball()
        move_player1()
        move_player2()

        # Check for winning condition
        if player1_score >= points_to_win:
            winner = "Player 1"
            break
        elif player2_score >= points_to_win:
            winner = "Player 2"
            break

        # Drawing on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1_paddle)
        pygame.draw.rect(screen, WHITE, player2_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        display_score()

        # Update the window
        pygame.display.flip()
        clock.tick(60)

    # Show winner screen
    show_winner_screen(winner)

# Function to display the winner screen and allow players to restart or quit
def show_winner_screen(winner):
    running = True
    while running:
        screen.fill(BLACK)

        winner_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))

        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    points_to_win = show_menu()
                    game_loop(points_to_win)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Show the menu first
points_to_win = show_menu()
# Start the game with the selected points to win
game_loop(points_to_win)
