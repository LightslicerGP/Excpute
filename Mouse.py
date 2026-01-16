import Port
import pygame

# Mapping mouse buttons to their respective bitmasks
mouse_bitmasks = {
    pygame.BUTTON_LEFT: [8, 0b10000000],
    pygame.BUTTON_MIDDLE: [8, 0b01000000],
    pygame.BUTTON_RIGHT: [8, 0b00100000],
    pygame.BUTTON_X1: [8, 0b00010000],  # Side button 1
    pygame.BUTTON_X2: [8, 0b00001000],  # Side button 2
}

# Bitmask for mouse wheel scroll up/down (stored in a different index for clarity)
scroll_bitmasks = {
    "up": [8, 0b00000100],  # Scroll up
    "down": [8, 0b00000010],  # Scroll down
}

# Use a global variable to maintain the scrolling state across function calls
scrolling = False

def handle_mouse_event(event, scale):
    global scrolling

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button in mouse_bitmasks:
            index, bitmask = mouse_bitmasks[event.button]
            Port.Ports[index] ^= bitmask  # Toggle the bitmask

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button in mouse_bitmasks:
            index, bitmask = mouse_bitmasks[event.button]
            Port.Ports[index] &= ~bitmask  # Clear the bitmask

    # Handle scroll events
    if event.type == pygame.MOUSEWHEEL:
        if not scrolling:
            scrolling = True
            # print("scrollweel")
            if event.y > 0:  # Scroll up
                index, bitmask = scroll_bitmasks["up"]
                Port.Ports[index] ^= bitmask  # Set the scroll up bitmask
            elif event.y < 0:  # Scroll down
                index, bitmask = scroll_bitmasks["down"]
                Port.Ports[index] ^= bitmask  # Set the scroll down bitmask
            
        elif scrolling:
            scrolling = False
            # print("scrollweel2")
            index, up_bitmask = scroll_bitmasks["up"]
            index, down_bitmask = scroll_bitmasks["down"]
            if Port.Ports[index] & 0b00000100:
                Port.Ports[index] &= ~up_bitmask  # Clear the scroll up bitmask
            elif Port.Ports[index] & 0b00000010:
                Port.Ports[index] &= ~down_bitmask  # Clear the scroll down bitmask

    # Update mouse pointer position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    Port.Ports[9] = int((mouse_x / (255 * scale)) * 255)
    Port.Ports[10] = 255 - int((mouse_y / (255 * scale)) * 255)
