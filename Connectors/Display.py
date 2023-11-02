import pygame
from PIL import Image, ImageDraw

# Initialize Pygame
pygame.init()

# Constants for image dimensions
WIDTH = 256
HEIGHT = 256

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create an empty PIL image
display = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(display)

# Function to put a pixel in the image


def putpixel(x, y, red, green, blue):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        draw.point((x, y), fill=(red, green, blue))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call your putpixel function to update specific pixel coordinates
    putpixel(0, 0, 255, 0, 0)
    putpixel(1, 1, 0, 255, 0)
    putpixel(255, 255, 0, 0, 255)

    # Convert PIL image to Pygame surface and display it
    pygame_img = pygame.image.fromstring(
        display.tobytes(), display.size, display.mode)
    screen.blit(pygame_img, (0, 0))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
