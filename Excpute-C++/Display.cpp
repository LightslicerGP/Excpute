#include <iostream>
#include <SDL2/SDL.h>
#include "RAM.h"
#include "Display.h"

using namespace std;

// SDL_Renderer *renderer = nullptr;
// int scale = 4;

// void display_refresh()
// {
//     int x = ram_read(252, false);
//     int y = ram_read(253, false);
//     uint8_t r = ram_read(249, false);
//     uint8_t g = ram_read(250, false);
//     uint8_t b = ram_read(251, false);
//     uint8_t mode = ram_read(254, false);

//     if (mode == 1)
//     {
//         SDL_SetRenderDrawColor(renderer, r, g, b, 255);
//         SDL_Rect pixelRect = {x * scale, y * scale, scale, scale};
//         SDL_RenderFillRect(renderer, &pixelRect);
//     }
//     else if (mode == 2)
//     {
//         SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
//         SDL_Rect pixelRect = {x * scale, y * scale, scale, scale};
//         SDL_RenderFillRect(renderer, &pixelRect);
//     }
//     else if (mode == 3)
//     {
//         // Fill screen with color data (not implemented)
//         SDL_SetRenderDrawColor(renderer, r, g, b, 255);
//         SDL_RenderClear(renderer);
//     }
// }

// void display_main()
// {
//     SDL_Init(SDL_INIT_VIDEO);

//     int resolutionX = 256;
//     int resolutionY = 256;
//     int width = resolutionX * scale;
//     int height = resolutionY * scale;

//     SDL_Window *window = SDL_CreateWindow("Display", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, 0);
//     renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED); // Create renderer inside main

//     SDL_DestroyRenderer(renderer);
//     SDL_DestroyWindow(window);
//     SDL_Quit();
// }

// void display_start()
// {
//     SDL_Event event;
//     bool running = true;

//     while (running)
//     {
//         while (SDL_PollEvent(&event))
//         {
//             if (event.type == SDL_QUIT)
//             {
//                 running = false;
//             }
//         }
//         SDL_RenderPresent(renderer);
//     }
// }

// SDL_Renderer *renderer;

void update_display(SDL_Renderer *renderer)
{
    int x = ram_read(253, false);
    int y = 255 - ram_read(254, false);
    int r = ram_read(250, false);
    int g = ram_read(251, false);
    int b = ram_read(252, false);
    int mode = ram_read(255, false);

    if (mode == 1)
    {
        // cout << "set color" << endl;
        // cout << "r:" << r << "g:" << g << "b:" << b << endl;

        SDL_Rect pixelRect = {x * scale, y * scale, scale, scale};
        SDL_SetRenderDrawColor(renderer, r, g, b, 255);
        SDL_RenderFillRect(renderer, &pixelRect);
    }
    else if (mode == 2)
    {
        // cout << "fill color" << endl;
        // cout << "r:" << r << " g:" << g << " b:" << b << endl;

        SDL_Rect fillRect = {0, 0, 256 * scale, 256 * scale};
        SDL_SetRenderDrawColor(renderer, r, g, b, 255);
        SDL_RenderFillRect(renderer, &fillRect);
    }
    else if (mode == 3)
    {
        // cout << "update buffer" << endl;

        SDL_RenderPresent(renderer);
    }

    ram_write(255, 0, false);
}