#include <iostream>
#include <array>

using namespace std;

array<int, 256> RAM = {0};

int ram_read(int id, bool signed_value = true)
{
    int value = RAM[id];
    if (!signed_value) // 0 to 255
        return value;
    if (value > 127) // when sig bit is 1, meaning negative
        return -(256 - value);
    else // when sig bit is 0, meaning positive
        return value;
}

void ram_write(int id, int new_data, bool signed_value = true)
{
    if (signed_value && -128 <= new_data && new_data < 0) // converts the negative number to unsigned number
        RAM[id] = 256 + new_data;
    else if ((!signed_value && 0 <= new_data && new_data <= 255) ||
             (signed_value && 0 <= new_data && new_data <= 127)) // sb doesn't matter, write number
        RAM[id] = new_data;
    else
        throw overflow_error("Cannot write " + to_string(new_data) + " to register " + to_string(id));
}