#include <SDL2/SDL.h>
#include "Keyboard.h"
#include "Mouse.h"

void Port_hardware(SDL_Event event, int scale) {
    Keyboard_handle_event(event);
    Mouse_handle_event(event, scale);
} 