// g++ -Isrc/include -Lsrc/lib temp.cpp -lmingw32 -lSDL2main -lSDL2
#include <iostream>
#include <SDL2/SDL.h>

int main(int argc, char *argv[])
{
    // Create a window and renderer
    SDL_Window *window = SDL_CreateWindow("Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 640, 480, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    bool answer = true;

    while (answer)
    {
        // Set the renderer draw color to white and clear the screen
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        SDL_RenderClear(renderer);

        // Update the screen with any rendering performed since the previous call
        SDL_RenderPresent(renderer);

        // Set the renderer draw color to black and clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Update the screen again to show the new color
        SDL_RenderPresent(renderer);
    }

    // Clean up resources before exiting
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);

    return 0;
}
