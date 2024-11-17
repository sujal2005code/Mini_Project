import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Define colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# Font setup
font = pygame.font.SysFont('Arial', 24)

# Load actual thumbnails (150x150 PNG images)
pong_thumbnail = pygame.image.load('menu_assets/pong_thumbnail.png')
pong_thumbnail = pygame.transform.scale(pong_thumbnail, (150, 150))

sudoku_thumbnail = pygame.image.load('menu_assets/sudoku_thumbnail.png')
sudoku_thumbnail = pygame.transform.scale(sudoku_thumbnail, (150, 150))

snake_thumbnail = pygame.image.load('menu_assets/snake_thumbnail.png')
snake_thumbnail = pygame.transform.scale(snake_thumbnail, (150, 150))

tic_tac_toe_thumbnail = pygame.image.load('menu_assets/tic_tac_toe_thumbnail.png')
tic_tac_toe_thumbnail = pygame.transform.scale(tic_tac_toe_thumbnail, (150, 150))

# Load background image and scale it to fit the window
background_image = pygame.image.load('menu_assets/background.png')  # Replace 'background.png' with your actual file name
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Game options with thumbnails
games = [
    {"name": "Pong", "script": "pong.py", "thumbnail": pong_thumbnail},
    {"name": "Sudoku", "script": "sudoku.py", "thumbnail": sudoku_thumbnail},
    {"name": "Snake", "script": "test.py", "thumbnail": snake_thumbnail},
    {"name": "Tic Tac Toe", "script": "tic_tac_toe.py", "thumbnail": tic_tac_toe_thumbnail}
]

# Button positions for 150x150 squares
button_positions = [
    (100, 100),
    (350, 100),
    (100, 350),
    (350, 350)
]

# Function to create a surface with rounded corners
def round_image(image, corner_radius):
    """Round the corners of an image surface."""
    size = image.get_size()
    
    # Create a new surface with per-pixel alpha
    rounded_image = pygame.Surface(size, pygame.SRCALPHA)
    
    # Create a mask with rounded corners
    mask = pygame.Surface(size, pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  # Transparent background
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=corner_radius)
    
    # Blit the original image onto the rounded mask
    rounded_image.blit(image, (0, 0))
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return rounded_image

# Function to draw rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    """Draw a rectangle with rounded corners."""
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_menu():
    for i, game in enumerate(games):
        x, y = button_positions[i]
        
        # Define the rect for the box and the corner radius
        rect = pygame.Rect(x, y, 150, 150)
        corner_radius = 20  # Radius of the rounded corners
        
        # Draw rounded rectangle (box)
        draw_rounded_rect(screen, WHITE, rect, corner_radius)
        
        # Round the corners of the image
        rounded_thumbnail = round_image(game["thumbnail"], corner_radius)
        
        # Blit the rounded thumbnail inside the rounded rectangle
        thumbnail_rect = rounded_thumbnail.get_rect(center=rect.center)
        screen.blit(rounded_thumbnail, thumbnail_rect.topleft)
        
        # Draw the game name below the rounded rectangle
        text = font.render(game["name"], True, BLACK)
        screen.blit(text, (x + (150 - text.get_width()) // 2, y + 160))  # Adjust text position

def launch_game(script):
    subprocess.Popen(["python", script])

# Game loop
running = True
while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))
    
    # Draw the menu with rounded images inside rounded boxes
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if a button is clicked (for 150x150 squares)
            for i, (x, y) in enumerate(button_positions):
                if x <= mouse_pos[0] <= x + 150 and y <= mouse_pos[1] <= y + 150:
                    launch_game(games[i]["script"])

    pygame.display.update()

# Quit Pygame
pygame.quit()
