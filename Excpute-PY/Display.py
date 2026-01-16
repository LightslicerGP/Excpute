import pygame
import RAM


def init_display(scale):
    resolutionX = 256
    resolutionY = 256
    width = resolutionX * scale
    height = resolutionY * scale

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.mouse.set_visible(False)
    # clock = pygame.time.Clock()
    return screen



def update_display(screen, scale):
    x = RAM.read(253, False)
    y = 255 - RAM.read(254, False)
    r = RAM.read(250, False)
    g = RAM.read(251, False)
    b = RAM.read(252, False)
    mode = RAM.read(255)
    
    if mode == 1:
        # print("set color")
        pixel_color = (r, g, b)
        pixel_rect = pygame.Rect(x * scale, y * scale, scale, scale)
        pygame.draw.rect(screen, pixel_color, pixel_rect)
    elif mode == 2:
        # print("fill color")
        pixel_color = (r, g, b)
        screen.fill(pixel_color)
    elif mode == 3:
        # print("update buffer")
        pygame.display.flip()
    RAM.write(255, 0, False)