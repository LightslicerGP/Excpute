import pygame
import RAM

pygame.init()
resolution = (256, 256)
scale = 4
width, height = resolution[0] * scale, resolution[1] * scale
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def refresh():
    x = RAM.read(252, False)
    y = RAM.read(253, False)
    r = RAM.read(249, False)
    g = RAM.read(250, False)
    b = RAM.read(251, False)
    mode = RAM.read(254)
    print(mode)
    if mode == 1:
        print(r, g, b, x, y)
        pixel_color = (r, g, b)
        pixel_rect = pygame.Rect(x * scale, y * scale, scale, scale)
        pygame.draw.rect(screen, pixel_color, pixel_rect)
    elif mode == 2:
        pixel_color = (0, 0, 0)
        pixel_rect = pygame.Rect(x * scale, y * scale, scale, scale)
        pygame.draw.rect(screen, pixel_color, pixel_rect)
    elif mode == 3:
        print("fill screen with color data")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add your display refresh logic here

    pygame.display.flip()


pygame.quit()
