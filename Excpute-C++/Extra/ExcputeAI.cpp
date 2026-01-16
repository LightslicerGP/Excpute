#include <thread>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#include "Display.h"
#include "Port.h"
#include "RAM.h"

std::vector<int> registers(8, 0);
bool debug = false;
bool print_registers = false;
int instruction_address = 0;

int reg_read(int id, bool signed = true)
{
    int value = registers[id];
    if (!signed)
    {
        return value;
    }
    if (value > 127)
    {
        return -(256 - value);
    }
    else
    {
        return value;
    }
}

void reg_write(int id, int new_data, bool signed = true)
{
    if (signed && -128 <= new_data < 0)
    {
        registers[id] = 256 + new_data;
    }
    else if ((!signed && 0 <= new_data <= 255) || (signed && 0 <= new_data <= 127))
    {
        registers[id] = new_data;
    }
    else
    {
        throw std::overflow_error("Cannot write " + std::to_string(new_data) + " to register " + std::to_string(id));
    }
}

void display_start()
{
    Display::start();
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
    // Implementation
}

void sub_op(int regA, int regB, int regDest, int SetFlag)
{
    // Implementation
}

void mul_op(int regA, int regB, int regDest, int SetFlag)
{
    // Implementation
}

void dvs_op(int regA, int regB, int regDest)
{
    // Implementation
}

void sqa_op(int regA, int regB, int regDest, int SetFlag)
{
    // Implementation
}

void sqr_op(int regA, int regB, int regDest)
{
    // Implementation
}

void orr_op(int regA, int regB, int regDest)
{
    // Implementation
}

void and_op(int regA, int regB, int regDest)
{
    // Implementation
}

void xor_op(int regA, int regB, int regDest)
{
    // Implementation
}

void inv_op(int regA, int regDest)
{
    // Implementation
}

void inc_op(int regA, int regDest)
{
    // Implementation
}

void dec_op(int regA, int regDest)
{
    // Implementation
}

void rsh_op(int regA, int regDest)
{
    // Implementation
}

void lsh_op(int regA, int regDest, int SetFlag)
{
    // Implementation
}

void rbs_op(int regA, int regDest)
{
    // Implementation
}

void lbs_op(int regA, int regDest)
{
    // Implementation
}

void cmp_op(int regA, int regB)
{
    // Implementation
}

void psh_op(int regA)
{
    // Implementation
}

void pop_op(int regDest)
{
    // Implementation
}

void cal_op(int jump_to)
{
    // Implementation
}

void rtn_op()
{
    // Implementation
}

void cpy_op(int regA, int regDest)
{
    // Implementation
}

void ldi_op(int address, int number)
{
    // Implementation
}

void lod_op(int regA, int regDest)
{
    // Implementation
}

void str_op(int regA, int regDest)
{
    // Implementation
}

void pti_op(int address, int regDest)
{
    // Implementation
}

void pto_op(int regA, int address)
{
    // Implementation
}

void jmp_op(int address)
{
    // Implementation
}

void jiz_op(int regA, int address)
{
    // Implementation
}

void spd_op(int regA, int property)
{
    // Implementation
}

std::map<std::string, std::function<void(int, int, int, int, int)>> instructions = {
    {"NOP", [](int, int, int, int, int)
     { return; }},
    {"HLT", hlt_op},
    {"ADD", add_op},
    {"SUB", sub_op},
    {"MUL", mul_op},
    {"DVS", dvs_op},
    {"SQA", sqa_op},
    {"SQR", sqr_op},
    {"ORR", orr_op},
    {"AND", and_op},
    {"XOR", xor_op},
    {"INV", inv_op},
    {"INC", inc_op},
    {"DEC", dec_op},
    {"RSH", rsh_op},
    {"LSH", lsh_op},
    {"RBS", rbs_op},
    {"LBS", lbs_op},
    {"CMP", cmp_op},
    {"PSH", psh_op},
    {"POP", pop_op},
    {"CAL", cal_op},
    {"RTN", rtn_op},
    {"CPY", cpy_op},
    {"LDI", ldi_op},
    {"LOD", lod_op},
    {"STR", str_op},
    {"PTI", pti_op},
    {"PTO", pto_op},
    {"JMP", jmp_op},
    {"JIZ", jiz_op},
    {"SPD", spd_op},
};

std::vector<std::vector<int>> get_instructions(const std::string &file)
{
    // Implementation
}

int main()
{
    std::vector<std::vector<int>> program = get_instructions("Instructions Compiled");
    while (instruction_address < program.size())
    {
        std::vector<int> instruction = program[instruction_address];
        if (debug || print_registers)
        {
            for (int i = 0; i < registers.size(); i++)
            {
                std::cout << registers[i] << " ";
            }
            std::cout << std::endl;
        }
        std::string op = instruction[0];
        std::vector<int> args(instruction.begin() + 1, instruction.end());
        instructions[op](args[0], args[1], args[2], args[3], args[4]);
        instruction_address = reg_read(7, false);
    }
    return 0;
}
