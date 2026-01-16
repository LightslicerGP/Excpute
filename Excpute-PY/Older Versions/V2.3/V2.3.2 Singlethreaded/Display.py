import pygame
import RAM


def init_display(scale):
    resolutionX = 256
    resolutionY = 256
    width = resolutionX * scale
    height = resolutionY * scale

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    # clock = pygame.time.Clock()
    return screen


def update_display(screen, scale):
    x = RAM.read(252, False)
    y = RAM.read(253, False)
    r = RAM.read(249, False)
    g = RAM.read(250, False)
    b = RAM.read(251, False)
    mode = RAM.read(254)
    if mode == 1:
        # print("set color")
        pixel_color = (r, g, b)
        pixel_rect = pygame.Rect(x * scale, y * scale, scale, scale)
        pygame.draw.rect(screen, pixel_color, pixel_rect)
    elif mode == 2:
        # print("reset color")
        pixel_color = (0, 0, 0)
        pixel_rect = pygame.Rect(x * scale, y * scale, scale, scale)
        pygame.draw.rect(screen, pixel_color, pixel_rect)
    elif mode == 3:
        # print("fill color")
        pixel_color = (r, g, b)
        # pixel_rect = pygame.Rect(0, 0, 256 * scale, 256 * scale)
        # pygame.draw.rect(screen, pixel_color, pixel_rect)
        screen.fill(pixel_color)
    RAM.write(254, 0, True)
