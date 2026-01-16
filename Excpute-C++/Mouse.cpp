#include <iostream>
#include <functional>
#include <SDL2/SDL.h>
#include "Ports.h"

using namespace std;

unordered_map<uint32_t, pair<int, uint8_t>> mouse_bitmasks = {
    {SDL_BUTTON_LEFT, {8, 0b10000000}},
    {SDL_BUTTON_MIDDLE, {8, 0b01000000}},
    {SDL_BUTTON_RIGHT, {8, 0b00100000}},
    {SDL_BUTTON_X1, {8, 0b00010000}},
    {SDL_BUTTON_X2, {8, 0b00001000}}};

unordered_map<string, pair<int, uint8_t>> scroll_bitmasks = {
    {"up", {8, 0b00000100}},
    {"down", {8, 0b00000010}}};

bool scrolling = false;

void Mouse_handle_event(SDL_Event event, int scale)
{
    if (event.type == SDL_MOUSEBUTTONDOWN)
    {
        if (mouse_bitmasks.count(event.button.button))
        {
            auto [index, bitmask] = mouse_bitmasks[event.button.button];
            Port[index] ^= bitmask; // Toggle the bitmask
        }
    }
    else if (event.type == SDL_MOUSEBUTTONUP)
    {
        if (mouse_bitmasks.count(event.button.button))
        {
            auto [index, bitmask] = mouse_bitmasks[event.button.button];
            Port[index] &= ~bitmask; // Clear the bitmask
        }
    }

    if (event.type == SDL_MOUSEWHEEL)
    {
        if (!scrolling)
        {
            scrolling = true;
            if (event.wheel.y > 0)
            { // Scroll up
                auto [index, bitmask] = scroll_bitmasks["up"];
                Port[index] ^= bitmask; // Set the scroll up bitmask
            }
            else if (event.wheel.y < 0)
            { // Scroll down
                auto [index, bitmask] = scroll_bitmasks["down"];
                Port[index] ^= bitmask; // Set the scroll down bitmask
            }
        }
        else
        {
            scrolling = false;
            auto [index, up_bitmask] = scroll_bitmasks["up"];
            auto [_, down_bitmask] = scroll_bitmasks["down"];
            if (Port[index] & 0b00000100)
            {
                Port[index] &= ~up_bitmask; // Clear the scroll up bitmask
            }
            else if (Port[index] & 0b00000010)
            {
                Port[index] &= ~down_bitmask; // Clear the scroll down bitmask
            }
        }
    }

    int mouse_x, mouse_y;
    SDL_GetMouseState(&mouse_x, &mouse_y);
    Port[9] = static_cast<int>((mouse_x / (255.0 * scale)) * 255);
    Port[10] = 255 - static_cast<int>((mouse_y / (255.0 * scale)) * 255);
}
