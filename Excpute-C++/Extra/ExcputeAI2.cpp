#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <map>
#include <stdexcept>
#include <bitset>
#include <sstream>

// #include "Display.h"
// #include "Port.h"
// #include "RAM.h"

std::vector<int> registers(8, 0);
bool debug = false;
bool print_registers = false;
int instruction_address = 0;

// void display_start()
// {
//     Display::start();
// }

int reg_read(int id, bool signed_flag = true)
{
    int value = registers[id];
    if (!signed_flag)
    {
        return value;
    }
    return value > 127 ? -(256 - value) : value;
}

void reg_write(int id, int new_data, bool signed_flag = true)
{
    if (signed_flag && new_data < 0 && new_data >= -128)
    {
        registers[id] = 256 + new_data;
    }
    else if ((!signed_flag && new_data >= 0 && new_data <= 255) || (signed_flag && new_data >= 0 && new_data <= 127))
    {
        registers[id] = new_data;
    }
    else
    {
        throw std::overflow_error("Cannot write " + std::to_string(new_data) + " to register " + std::to_string(id));
    }
}

int flag_read(const std::string &flag)
{
    std::map<std::string, int> flag_bits = {{"carry", -1}, {"zero", -2}, {"parity", -3}, {"negative", -4}};
    std::bitset<8> flag_byte(reg_read(6, false));

    if (flag_bits.find(flag) != flag_bits.end())
    {
        return flag_byte[flag_bits[flag]];
    }
    else
    {
        throw std::invalid_argument("Flag must be carry, zero, parity, overflow, or negative");
    }
}

void flag_set(const std::string &flag, int sign)
{
    std::map<std::string, int> flag_bits = {{"carry", -1}, {"zero", -2}, {"parity", -3}, {"negative", -4}, {"overflow", -5}};

    if (sign == 0 || sign == 1)
    {
        std::bitset<8> flag_byte(reg_read(6, false));

        if (flag_bits.find(flag) != flag_bits.end())
        {
            flag_byte[flag_bits[flag]] = sign;
            reg_write(6, static_cast<int>(flag_byte.to_ulong()), false);
        }
        else
        {
            throw std::invalid_argument("Flag must be carry, zero, parity, overflow, or negative");
        }
    }
    else
    {
        throw std::invalid_argument("flag_write number must be 1 or 0");
    }
}

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

void hlt_op()
{
    if (debug)
    {
        std::cout << instruction_address << ": Halt Operation" << std::endl;
    }
    exit(0);
}

void add_op(int regA, int regB, int regDest, int SetFlag, int CarryFlag)
{
    if (debug)
    {
        std::cout << instruction_address << ": Addition" << std::endl;
    }
    int A = reg_read(regA, true);
    int B = reg_read(regB, true);

    int result = CarryFlag == 1 ? A + B + flag_read("carry") : A + B;

    if (!(result >= -128 && result <= 127))
    {
        if (SetFlag == 1)
        {
            flag_set("carry", 1);
        }
        result = static_cast<int>(std::bitset<8>(result).to_ulong());
    }
    reg_write(regDest, result);
    next_instruction();
}

// Define other operations (sub_op, mul_op, dvs_op, etc.) similarly...

std::vector<std::tuple<std::string, std::vector<int>>> get_instructions(const std::string &file)
{
    std::ifstream instruction_file(file);
    std::string line;
    std::vector<std::tuple<std::string, std::vector<int>>> instruction_array;

    while (std::getline(instruction_file, line))
    {
        std::istringstream iss(line);
        std::vector<int> args;
        std::string operation;
        iss >> operation;

        std::string item;
        while (iss >> item)
        {
            if (std::regex_match(item, std::regex("^-?\\d+$")))
            {
                args.push_back(std::stoi(item));
            }
            else
            {
                operation = item;
            }
        }

        instruction_array.push_back(std::make_tuple(operation, args));
    }

    for (const auto &inst : instruction_array)
    {
        std::cout << std::get<0>(inst) << " ";
        for (const auto &arg : std::get<1>(inst))
        {
            std::cout << arg << " ";
        }
        std::cout << std::endl;
    }

    return instruction_array;
}

int main()
{
    // std::thread(display_start).detach();
    instruction_address = reg_read(7, false);
    reg_write(7, 0, false);   // set instruction address
    reg_write(5, 248, false); // set stack address

    std::map<std::string, std::function<void(std::vector<int>)>> instructions = {
        {"NOP", [](std::vector<int>) {}},
        {"HLT", [](std::vector<int>)
         { hlt_op(); }},
        {"ADD", [](std::vector<int> args)
         { add_op(args[0], args[1], args[2], args.size() > 3 ? args[3] : 1, args.size() > 4 ? args[4] : 0); }},
        // Define other operations similarly...
    };

    std::vector<std::tuple<std::string, std::vector<int>>> program = get_instructions("Instructions Compiled");

    while (instruction_address < 256)
    {
        try
        {
            auto instruction = program.at(instruction_address);
            std::string op = std::get<0>(instruction);
            std::vector<int> args = std::get<1>(instruction);

            if (debug || print_registers)
            {
                for (const auto &reg : registers)
                {
                    std::cout << reg << " ";
                }
                std::cout << std::endl;
            }

            instructions[op](args);
            instruction_address = reg_read(7, false);
        }
        catch (std::out_of_range &)
        {
            std::cout << "Ran out of instructions, halted automatically" << std::endl;
            if (debug)
            {
                std::cout << "Instruction address: " << instruction_address << std::endl;
            }
            exit(0);
        }
    }

    return 0;
}
