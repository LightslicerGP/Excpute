# import pygame
# import sys
# import colorsys

# # Initialize pygame
# pygame.init()

# # Set up display
# logical_resolution = (256, 256)
# display_scale = 5
# width, height = logical_resolution[0] * display_scale, logical_resolution[1] * display_scale
# screen = pygame.display.set_mode((width, height), flags=pygame.SRCALPHA)
# pygame.display.set_caption("Moving Rainbow Gradient Display")

# # Create a clock to control the frame rate
# clock = pygame.time.Clock()

# # Initialize variables
# gradient_offset = 0.0

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill((0, 0, 0, 0))

#     # Draw moving rainbow gradient
#     for y in range(logical_resolution[1]):
#         hue = ((y + gradient_offset) / logical_resolution[1]) * 360.0
#         color = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)

#         # Draw at a higher resolution
#         for dy in range(display_scale):
#             pygame.draw.line(
#                 screen,
#                 (color[0] * 255, color[1] * 255, color[2] * 255),
#                 (0, y * display_scale + dy),
#                 (width, y * display_scale + dy)
#             )

#     # Update the display
#     pygame.display.flip()

#     # Increment the gradient offset for movement
#     gradient_offset += 0

#     # Cap the frame rate
#     clock.tick(60)

# # Quit pygame
# pygame.quit()
# sys.exit()
