// g++ -std=c++20 -Isrc/Include -Lsrc/lib -O3 -o Excpute Excpute.cpp RAM.cpp Display.cpp -lmingw32 -lSDL2main -lSDL2
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <array>
#include <functional>
#include <bitset>
#include <fstream>
#include <tuple>
#include <regex>
#include <sstream>
#include <thread>
#include <SDL2/SDL.h>
#include "RAM.h"
#include "Ports.h"
#include "Display.h"

using namespace std;

int instruction_address;
constexpr bool debug = false;

SDL_Window *window;

// SDL_Renderer *renderer;

enum Flag
{
    carry,
    zero,
    parity,
    negative,
    overflow
};

array<int, 8> registers = {0};

int reg_read(int id, bool signed_value = true)
{
    int value = registers[id];
    if (!signed_value) // 0 to 255
        return value;
    if (value > 127) // when sig bit is 1, meaning negative
        return -(256 - value);
    else // when sig bit is 0, meaning positive
        return value;
}

void reg_write(int id, int new_data, bool signed_value = true)
{
    if (signed_value && -128 <= new_data && new_data < 0) // converts the negative number to unsigned number
        registers[id] = 256 + new_data;
    else if ((not signed_value && 0 <= new_data && new_data <= 255) ||
             (signed_value && 0 <= new_data && new_data <= 127)) // sb doesn't matter, write number
        registers[id] = new_data;
    else
        throw overflow_error("Cannot write " + to_string(new_data) + " to register " + to_string(id));
}

// array<int, 256> RAM = {0};

// int ram_read(int id, bool signed_value = true)
// {
//     int value = RAM[id];
//     if (!signed_value) // 0 to 255
//         return value;
//     if (value > 127) // when sig bit is 1, meaning negative
//         return -(256 - value);
//     else // when sig bit is 0, meaning positive
//         return value;
// }

// void ram_write(int id, int new_data, bool signed_value = true)
// {
//     if (signed_value && -128 <= new_data && new_data < 0) // converts the negative number to unsigned number
//         RAM[id] = 256 + new_data;
//     else if ((not signed_value && 0 <= new_data && new_data <= 255) ||
//              (signed_value && 0 <= new_data && new_data <= 127)) // sb doesn't matter, write number
//         RAM[id] = new_data;
//     else
//         throw overflow_error("Cannot write " + to_string(new_data) + " to register " + to_string(id));
// }

// array<int, 256> Port = {0};

// int port_read(int id, bool signed_value = true)
// {
//     int value = Port[id];
//     if (!signed_value) // 0 to 255
//         return value;
//     if (value > 127) // when sig bit is 1, meaning negative
//         return -(256 - value);
//     else // when sig bit is 0, meaning positive
//         return value;
// }

// void port_write(int id, int new_data, bool signed_value = true)
// {
//     if (signed_value && -128 <= new_data && new_data < 0) // converts the negative number to unsigned number
//         Port[id] = 256 + new_data;
//     else if ((not signed_value && 0 <= new_data && new_data <= 255) ||
//              (signed_value && 0 <= new_data && new_data <= 127)) // sb doesn't matter, write number
//         Port[id] = new_data;
//     else
//         throw overflow_error("Cannot write " + to_string(new_data) + " to register " + to_string(id));
// }

int flag_read(Flag flag)
{
    switch (flag)
    {
    case carry:
        return reg_read(6, false) & 0b00000001;
    case zero:
        return reg_read(6, false) & 0b00000010;
    case parity:
        return reg_read(6, false) & 0b00000100;
    case negative:
        return reg_read(6, false) & 0b00001000;
    case overflow:
        return reg_read(6, false) & 0b00010000;
    default:
        throw invalid_argument("Flag must be carry, zero, parity, overflow, or negative");
    }
}
void flag_set(Flag flag, int sign)
{
    if (sign == 0)
    {
        switch (flag)
        {
        case carry:
            reg_write(6, reg_read(6, false) & 0b11111110, false);
            break;
        case zero:
            reg_write(6, reg_read(6, false) & 0b11111101, false);
            break;
        case parity:
            reg_write(6, reg_read(6, false) & 0b11111011, false);
            break;
        case negative:
            reg_write(6, reg_read(6, false) & 0b11110111, false);
            break;
        case overflow:
            reg_write(6, reg_read(6, false) & 0b11101111, false);
            break;
        default:
            throw invalid_argument("Flag must be carry, zero, parity, overflow, or negative");
        }
    }
    else if (sign == 1)
    {
        switch (flag)
        {
        case carry:
            reg_write(6, reg_read(6, false) | 0b00000001, false);
            break;
        case zero:
            reg_write(6, reg_read(6, false) | 0b00000010, false);
            break;
        case parity:
            reg_write(6, reg_read(6, false) | 0b00000100, false);
            break;
        case negative:
            reg_write(6, reg_read(6, false) | 0b00001000, false);
            break;
        case overflow:
            reg_write(6, reg_read(6, false) | 0b00010000, false);
            break;
        default:
            throw invalid_argument("Flag must be carry, zero, parity, overflow, or negative");
        }
    }

    else
    {
        throw invalid_argument("flag_writ e number must be 1 or 0");
    }
}

// void display_start()
// {
// }

// void display_refresh()
// {
//     int x = ram_read(252, false);
//     int y = ram_read(253, false);
//     int r = ram_read(249, false);
//     int g = ram_read(250, false);
//     int b = ram_read(251, false);
//     int mode = ram_read(254);
//     if (mode == 1)
//     {
//         array pixel_color = {r, g, b};
//     }
//     else if (mode == 2)
//     {
//         /* code */
//     }
//     else if (mode == 3)
//     {
//         cout << "fill screen with color data" << endl;
//     }
// }

void next_instruction()
{
    if (instruction_address == 255)
    {
        reg_write(7, 0, false);
    }
    else
    {
        reg_write(7, instruction_address + 1, false);
    }
}
unordered_map<string, int> opcode_map = {
    {"NOP", 0},
    {"HLT", 1},
    {"ADD", 2},
    {"SUB", 3},
    {"MLT", 4},
    {"DVS", 5},
    {"SQA", 6},
    {"SQR", 7},
    {"ORR", 8},
    {"AND", 9},
    {"XOR", 10},
    {"INV", 11},
    {"INC", 12},
    {"DEC", 13},
    {"RSH", 14},
    {"LSH", 15},
    {"RBS", 16},
    {"LBS", 17},
    {"CMP", 18},
    {"PSH", 19},
    {"POP", 20},
    {"CAL", 21},
    {"RTN", 22},
    {"CPY", 23},
    {"LDI", 24},
    {"LOD", 25},
    {"STR", 26},
    {"PTI", 27},
    {"PTO", 28},
    {"JMP", 29},
    {"JIZ", 30},
    {"SPD", 31},
};

void execute(string opcode, vector<int> operands, SDL_Renderer *renderer)
{
    auto it = opcode_map.find(opcode);
    if (it == opcode_map.end())
    {
        throw invalid_argument("Invalid opcode");
    }
    switch (it->second)
    {
    case 0: // NOP
        next_instruction();
        break;
    case 1: // HLT
        if (debug)
        {
            cout << instruction_address << ": Halt Operation" << endl;
        }
        exit(0);
        break;
    case 2: // ADD
        if (debug)
        {
            cout << instruction_address << ": Addition" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];
            int regDest = operands[2];
            int SetFlag = (operands.size() > 3) ? operands[3] : 0;
            int CarryFlag = (operands.size() > 4) ? operands[4] : 0;

            int A = reg_read(regA, false);
            int B = reg_read(regB, false);
            int result;

            if (CarryFlag == 1)
            {
                result = A + B + flag_read(carry);
            }
            else
            {
                result = A + B;
            }

            if (result > 255)
            {
                if (SetFlag == 1)
                {
                    flag_set(carry, 1);
                }
                result -= 256;
            }

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 3: // SUB
        if (debug)
        {
            cout << instruction_address << ": Subtraction" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];
            int regDest = operands[2];
            int SetFlag = (operands.size() > 3) ? operands[3] : 0;

            int A = reg_read(regA, true);
            int B = reg_read(regB, true);

            int result = A - B;

            if (result > 127)
            {
                result -= 256;
            }
            else if (result < -128)
            {
                if (SetFlag == 1)
                {
                    flag_set(carry, 1);
                }
                result += 256;
            }

            reg_write(regDest, result);
            next_instruction();
        }
        break;
    case 8: // ORR
        if (debug)
        {
            cout << instruction_address << ": Or" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];
            int regDest = operands[2];

            int A = reg_read(regA, false);
            int B = reg_read(regB, false);

            int result = A | B;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 9: // AND
        if (debug)
        {
            cout << instruction_address << ": And" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];
            int regDest = operands[2];

            int A = reg_read(regA, false);
            int B = reg_read(regB, false);

            int result = A & B;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 10: // XOR
        if (debug)
        {
            cout << instruction_address << ": Xor" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];
            int regDest = operands[2];

            int A = reg_read(regA, false);
            int B = reg_read(regB, false);

            int result = A ^ B;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 11: // INV
        if (debug)
        {
            cout << instruction_address << ": Invert" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA, false);

            int result = A ^ 255;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 12: // INC
        if (debug)
        {
            cout << instruction_address << ": Increment" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];
            int SetFlag = (operands.size() > 2) ? operands[2] : 1;

            int A = reg_read(regA, false);
            int result;

            if (A == 255)
            {
                if (SetFlag == 1)
                {
                    flag_set(carry, 1);
                }
                result = 0;
            }
            else
            {
                result = A + 1;
            }

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 13: // DEC
        if (debug)
        {
            cout << instruction_address << ": Decrement" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA, false);
            int result;

            if (A == 0)
            {
                result = 255;
            }
            else
            {
                result = A - 1;
            }

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 14: // RSH
        if (debug)
        {
            cout << instruction_address << ": Right shift" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA, false);

            int result = A >> 1;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 15: // LSH
        if (debug)
        {
            cout << instruction_address << ": Left shift" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];
            int SetFlag = operands[2];

            int A = reg_read(regA, false);

            int result = A << 1;

            if (result > 255)
            {
                if (SetFlag == 1)
                {
                    flag_set(carry, 1);
                }
                result -= 256;
            }

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 16: // RBS
        if (debug)
        {
            cout << instruction_address << ": Right barrel shift" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA, false);

            int result = (A >> 1) | (A << 7) & 255;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 17: // LBS
        if (debug)
        {
            cout << instruction_address << ": Left barrel shift" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA, false);

            int result = ((A << 1) | (A >> 7)) & 255;

            reg_write(regDest, result, false);
            next_instruction();
        }
        break;
    case 18: // CMP
        if (debug)
        {
            cout << instruction_address << ": Compare" << endl;
        }
        {
            int regA = operands[0];
            int regB = operands[1];

            int A = reg_read(regA);
            int B = reg_read(regB);

            int result = B - A;

            if (debug)
            {
                cout << A << " ? " << B << " = " << result << endl;
            }

            if (result == 0)
            {
                if (debug)
                {
                    cout << "ZERO FLAG" << endl;
                }
                flag_set(zero, 1);
            }
            else
            {
                flag_set(zero, 0);
            }

            if (result > 0)
            {
                if (debug)
                {
                    cout << "NEG FLAG" << endl;
                }
                flag_set(negative, 1);
            }
            else
            {
                flag_set(negative, 0);
            }

            if (result < 0)
            {
                if (debug)
                {
                    cout << "CARRY FLAG" << endl;
                }
                flag_set(carry, 1);
            }
            else
            {
                flag_set(carry, 0);
            }

            next_instruction();
        }
        break;
    case 19: // PSH
        if (debug)
        {
            cout << instruction_address << ": Push to stack" << endl;
        }
        {
            int regA = operands[0];

            int A = reg_read(regA, false);
            int stack_pointer = reg_read(5, false);

            ram_write(stack_pointer, A, false);     // writes to stack
            reg_write(5, stack_pointer - 1, false); // "increments" (decrements) pointer
            next_instruction();
        }
        break;
    case 20: // POP
        if (debug)
        {
            cout << instruction_address << ": Pop from stack" << endl;
        }
        {
            int regDest = operands[0];

            int stack_pointer = reg_read(5, false);

            int pointer_data = ram_read(stack_pointer + 1, false); // reads last pointer location
            reg_write(regDest, pointer_data, false);               // writes from stack
            reg_write(5, stack_pointer + 1, false);                // "decrements" (increments) pointer

            next_instruction();
        }
        break;
    case 21: // CAL
        if (debug)
        {
            cout << instruction_address << ": Call from stack" << endl;
        }
        {
            int jump_to = operands[0];

            int stack_pointer = reg_read(5, false);

            ram_write(stack_pointer, instruction_address + 1, false); // writes to stack
            reg_write(5, stack_pointer - 1, false);                   // "increments" (decrements) pointer
            reg_write(7, jump_to, false);                             // jumps to new instruction address
            // instead of running next_instruction()
        }
        break;
    case 22: // RTN
        if (debug)
        {
            cout << instruction_address << ": Return from stack" << endl;
        }
        {
            int stack_pointer = reg_read(5, false);
            int pointer_data = ram_read(stack_pointer + 1, false); // reads last pointer location
            reg_write(5, stack_pointer + 1, false);                // "decrements" (increments) pointer
            // is this neccessary? - no RAM.write(stack_pointer + 1, 0, False)  // writes 0 to current pointer location
            reg_write(7, pointer_data, false); // returns to the instruction adress
        }
        break;
    case 23: // CPY
        if (debug)
        {
            cout << instruction_address << ": Copy" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int data = reg_read(regA);

            reg_write(regDest, data);
            next_instruction();
        }
        break;
    case 24: // LDI
        if (debug)
        {
            cout << instruction_address << ": Load immediate" << endl;
        }
        {
            int address = operands[0];
            int number = operands[1];

            reg_write(address, number);
            next_instruction();
        }
        break;
    case 25: // LOD
        if (debug)
        {
            cout << instruction_address << ": Load from memory" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA);
            int data = ram_read(A);

            reg_write(regDest, data);
            next_instruction();
        }
        break;
    case 26: // STR
        if (debug)
        {
            cout << instruction_address << ": Store to memory" << endl;
        }
        {
            int regA = operands[0];
            int regDest = operands[1];

            int A = reg_read(regA);
            int Destination = reg_read(regDest, false);

            ram_write(Destination, A);
            next_instruction();
        }
        break;
    case 27: // PTI
        if (debug)
        {
            cout << instruction_address << ": Port input" << endl;
        }
        {
            int address = operands[0];
            int regDest = operands[1];

            int data = port_read(address);

            reg_write(regDest, data);
            next_instruction();
        }
        break;
    case 28: // PTO
        if (debug)
        {
            cout << instruction_address << ": Port output" << endl;
        }
        {
            int regA = operands[0];
            int address = operands[1];

            port_write(regA, address);
            next_instruction();
        }
        break;
    case 29: // JMP
        if (debug)
        {
            cout << instruction_address << ": Jump to instruction" << endl;
        }
        {
            int address = operands[0];

            reg_write(7, address, false);
        }
        break;
    case 30: // JIZ
        if (debug)
        {
            cout << instruction_address << ": Jump if zero" << endl;
        }
        {
            int regA = operands[0];
            int address = operands[1];

            int A = reg_read(regA);

            if (A == 0)
            {
                reg_write(7, address, false);
            }
            else
            {
                next_instruction();
            }
        }
        break;
    case 31: // SPD
        if (debug)
        {
            cout << instruction_address << ": Set pixel data" << endl;
        }
        {
            int regA = operands[0];
            int property = operands[1];
            int mode = (operands.size() > 2) ? operands[2] : 0;

            int A = reg_read(regA, false);

            if (mode == 0)
            {
                // cout << "Property number: " << property << endl;
                if (property < 5) // r, g, b, x, y
                {
                    int ram_address = property + 250; // 0 -> 250, 4 -> 254
                    ram_write(ram_address, A, false);
                }
                else if (property >= 5) // set, fill, update
                {
                    int ram_data = property - 4; // 5 -> 1, 7 -> 3
                    ram_write(255, ram_data, false);
                    update_display(renderer);
                }
            }
            else if (mode == 1)
            {
                int x_coordinate = ram_read(253, false) * scale;
                int y_coordinate = (255 - ram_read(254, false)) * scale;
                SDL_Color color;
                SDL_GetRenderDrawColor(renderer, &color.r, &color.g, &color.b, &color.a);

                if (property == 0) // red value
                {
                    reg_write(regA, color.r, false);
                }
                else if (property == 1) // green value
                {
                    reg_write(regA, color.g, false);
                }
                else if (property == 2) // blue value
                {
                    reg_write(regA, color.b, false);
                }
                else if ((property == 3) || (property == 4)) // x or y coordinate
                {
                    int ram_address = property + 250; // 3 -> 253, 4 -> 254
                    ram_write(ram_address, A, false);
                }
                else if (property >= 5) // set, fill, update
                {
                    cout << "mode is set/fill/push, and reading from screen?" << endl;
                }
            }

            next_instruction();
        }
        break;

    default:
        throw invalid_argument("Invalid opcode");
    }
}

vector<tuple<string, vector<int>>> get_instructions(const string &file_name)
{
    vector<tuple<string, vector<int>>> instruction_array;
    ifstream file(file_name);
    string str;
    vector<string> outer_vector;
    while (getline(file, str))
    {
        istringstream iss(str);
        vector<string> parts;
        string part;
        while (iss >> part)
        {
            parts.push_back(part);
        }
        string opcode = parts[0];
        vector<int> operands;
        for (int i = 1; i < parts.size(); i++)
        {
            try
            {
                operands.push_back(stoi(parts[i]));
            }
            catch (const invalid_argument &e)
            {
                cerr << "Invalid operand at line " << instruction_array.size() + 1 << ": " << parts[i] << endl;
                exit(1);
            }
        }
        tuple<string, vector<int>> instruction = make_tuple(opcode, operands);
        instruction_array.push_back(instruction);
    }

    // cout << "Returning instruction array" << endl;
    return instruction_array;
};

// int main(int argc, char *argv[])
// {
//     display_main();
//     instruction_address = reg_read(7, false);
//     reg_write(7, 0, false);   // set instruction address
//     reg_write(5, 248, false); // set stack address

//     vector<tuple<string, vector<int>>> program = get_instructions("Instructions Compiled");

//     while (instruction_address < 256)
//     {
//         try
//         {
//             string opcode = get<0>(program[instruction_address]);
//             vector<int> operands = get<1>(program[instruction_address]);
//             execute(opcode, operands);
//             cout << opcode << endl;
//             for (int i = 0; i < 8; i++)
//             {
//                 cout << "Register " << i << ": " << registers[i] << endl;
//             }
//         }
//         catch (const exception &e)
//         {
//             cout << "Ran out of instructions, halted automatically" << endl;
//             if (debug)
//             {
//                 cout << "Instruction address: " << instruction_address << endl;
//             }
//             exit(0);
//         }

//         // reg_write(7, reg_read(7, false) + 1, false);
//         instruction_address = reg_read(7, false);
//     }
//     return 0;
// }

SDL_Renderer *display_init()
{
    int resolutionX = 256;
    int resolutionY = 256;
    int width = resolutionX * scale;
    int height = resolutionY * scale;

    SDL_Window *window = SDL_CreateWindow("Display", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    return renderer;
}

void update_cpu(vector<tuple<string, vector<int>>> program, SDL_Renderer *renderer)
{

    if (instruction_address < 256)
    {
        string opcode = get<0>(program[instruction_address]);
        vector<int> operands = get<1>(program[instruction_address]);
        // cout << instruction_address << " " << opcode << endl;
        execute(opcode, operands, renderer);
        if (debug)
        {
            for (int i = 0; i < 8; i++)
            {
                cout << "Register " << i << ": " << bitset<8>(registers[i]) << " " << registers[i] << endl;
            }
        }

        instruction_address = reg_read(7, false);
    }
    else
    {
        cout << "Ran out of instructions, halted automatically" << endl;
        if (debug)
        {
            cout << "Instruction address: " << instruction_address << endl;
        }
        exit(0);
    }
}

int main(int argc, char *argv[])
{
    SDL_Init(SDL_INIT_EVERYTHING);

    SDL_Renderer *renderer = display_init();

    vector<tuple<string, vector<int>>> program = get_instructions("Instructions Compiled");
    // instruction_address = reg_read(7, false);
    reg_write(7, 0, false);   // set instruction address
    reg_write(5, 249, false); // set stack address

    bool running = true;

    SDL_Event event;

    while (running)
    {
        while (SDL_PollEvent(&event))
        {
            if (event.type == SDL_QUIT)
            {
                running = false;
            }
            Port_hardware(event, scale);
        }

        update_cpu(program, renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}