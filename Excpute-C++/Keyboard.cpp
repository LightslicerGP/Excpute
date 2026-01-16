#include <iostream>
#include <functional>
#include <SDL2/SDL.h>
#include "Ports.h"

using namespace std;

unordered_map<SDL_Keycode, pair<int, uint8_t>> key_bitmasks = {
    {SDLK_SPACE, {0, 0b10000000}},
    {SDLK_BACKQUOTE, {0, 0b01000000}},
    {SDLK_1, {0, 0b00100000}},
    {SDLK_2, {0, 0b00010000}},
    {SDLK_3, {0, 0b00001000}},
    {SDLK_4, {0, 0b00000100}},
    {SDLK_5, {0, 0b00000010}},
    {SDLK_6, {0, 0b00000001}},
    {SDLK_7, {1, 0b10000000}},
    {SDLK_8, {1, 0b01000000}},
    {SDLK_9, {1, 0b00100000}},
    {SDLK_0, {1, 0b00010000}},
    {SDLK_MINUS, {1, 0b00001000}},
    {SDLK_EQUALS, {1, 0b00000100}},
    {SDLK_q, {1, 0b00000010}},
    {SDLK_w, {1, 0b00000001}},
    {SDLK_e, {2, 0b10000000}},
    {SDLK_r, {2, 0b01000000}},
    {SDLK_t, {2, 0b00100000}},
    {SDLK_y, {2, 0b00010000}},
    {SDLK_u, {2, 0b00001000}},
    {SDLK_i, {2, 0b00000100}},
    {SDLK_o, {2, 0b00000010}},
    {SDLK_p, {2, 0b00000001}},
    {SDLK_LEFTBRACKET, {2, 0b00000001}},
    {SDLK_RIGHTBRACKET, {3, 0b10000000}},
    {SDLK_BACKSLASH, {3, 0b00100000}},
    {SDLK_a, {3, 0b00010000}},
    {SDLK_s, {3, 0b00001000}},
    {SDLK_d, {3, 0b00000100}},
    {SDLK_f, {3, 0b00000010}},
    {SDLK_g, {3, 0b00000001}},
    {SDLK_h, {4, 0b10000000}},
    {SDLK_j, {4, 0b01000000}},
    {SDLK_k, {4, 0b00100000}},
    {SDLK_l, {4, 0b00010000}},
    {SDLK_SEMICOLON, {4, 0b00001000}},
    {SDLK_QUOTE, {4, 0b00000100}},
    {SDLK_z, {4, 0b00000010}},
    {SDLK_x, {4, 0b00000001}},
    {SDLK_c, {5, 0b10000000}},
    {SDLK_v, {5, 0b01000000}},
    {SDLK_b, {5, 0b00100000}},
    {SDLK_n, {5, 0b00010000}},
    {SDLK_m, {5, 0b00001000}},
    {SDLK_COMMA, {5, 0b00000100}},
    {SDLK_PERIOD, {5, 0b00000010}},
    {SDLK_SLASH, {5, 0b00000001}},
    {SDLK_BACKSPACE, {6, 0b10000000}},
    {SDLK_TAB, {6, 0b01000000}},
    {SDLK_RETURN, {6, 0b00100000}},
    {SDLK_LSHIFT, {6, 0b00010000}}, // Combined Shift
    {SDLK_RSHIFT, {6, 0b00010000}}, // Combined Shift
    {SDLK_UP, {6, 0b00001000}},
    {SDLK_LEFT, {6, 0b00000100}},
    {SDLK_DOWN, {6, 0b00000010}},
    {SDLK_RIGHT, {6, 0b00000001}},
    {SDLK_CAPSLOCK, {7, 0b10000000}},
    {SDLK_LCTRL, {7, 0b01000000}}, // Combined Control
    {SDLK_RCTRL, {7, 0b01000000}}, // Combined Control
    {SDLK_LALT, {7, 0b00100000}},  // Combined Alt
    {SDLK_RALT, {7, 0b00100000}},  // Combined Alt
    {SDLK_ESCAPE, {7, 0b00010000}},
    {SDLK_PRINTSCREEN, {7, 0b00001000}},
    {SDLK_INSERT, {7, 0b00000100}},
    {SDLK_DELETE, {7, 0b00000010}}};

void Keyboard_handle_event(SDL_Event event)
{
    if (event.type == SDL_KEYDOWN)
    {
        auto it = key_bitmasks.find(event.key.keysym.sym);
        if (it != key_bitmasks.end())
        {
            int index = it->second.first;
            uint8_t bitmask = it->second.second;
            Port[index] ^= bitmask; // Toggle the bit
        }
    }
    else if (event.type == SDL_KEYUP)
    {
        auto it = key_bitmasks.find(event.key.keysym.sym);
        if (it != key_bitmasks.end())
        {
            int index = it->second.first;
            uint8_t bitmask = it->second.second;
            Port[index] &= ~bitmask; // Clear the bit
        }
    }
}