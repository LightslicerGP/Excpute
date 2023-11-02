# import Display
from Connectors import Config
import json

x = 0
y = 0
red = 0
blue = 0
green = 0
flag = 0
reg_len = Config.reg_len()

instructionlist = "binary instruction"


def bin2num(bin_str):
    try:
        return int(bin_str, 2)
    except ValueError:
        print(f"Invalid binary string: {bin_str}")
        return None

# not really used???


def num2bin(num, bits=8):
    try:
        binary_str = bin(num)[2:].zfill(bits)
        return binary_str
    except ValueError:
        print(f"Invalid decimal number: {num}")
        return None


def reg_read(id):
    id = str(bin2num(id))
    try:
        with open('Registers.json', "r") as register_file:
            registers = json.load(register_file)
        if id in registers:
            return registers[id]
        else:
            print(f"Register with ID {id} does not exist.")
            return None
    except FileNotFoundError:
        print("Registers file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return None


def reg_write(id, data):
    id_str = str(bin2num(id))
    try:
        with open('Registers.json', "r") as register_file:
            registers = json.load(register_file)
        registers[id_str] = data
        with open('Registers.json', "w") as register_file:
            json.dump(registers, register_file, indent=4)
    except FileNotFoundError:
        print("Registers file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")


with open(instructionlist, 'r') as f:
    file_contents = f.read()
instructions = [file_contents[i:i + 16]
                for i in range(0, len(file_contents), 16)]
print(instructions)

for instruction in instructions:
    flag = 0
    if instruction[:5] == '00000':
        # No operation
        print('hey, there is no operation lmao')
    elif instruction[:5] == '00001':
        # Halt
        print('Found instruction 00001, halting CPU.')
        break
    elif instruction[:5] == '00010':
        # Add
        reg_dest = instruction[5:8]
        flag_state = instruction[8:9]
        carry_state = instruction[9:10]
        reg_a = instruction[10:13]
        reg_b = instruction[13:16]
        reg_a_data = reg_read(reg_a)
        reg_b_data = reg_read(reg_b)
        result = bin(int(reg_a_data, 2) +
                     int(reg_b_data, 2))[2:].zfill(reg_len)
        print(f"Added register {int(reg_a, 2)} valued {int(reg_a_data, 2)} and register {int(reg_b, 2)} valued {int(reg_b_data, 2)} resulting {int(reg_a_data, 2) + int(reg_b_data, 2)} saving result in reg {int(reg_dest, 2)}")
        if len(result) == reg_len:
            reg_write(reg_dest, result)
        else:
            if flag_state == 1:
                flag = result[:1]
                result = result[1:]
                reg_write(reg_dest, result)
            elif flag_state == 0:
                result = result[1:]
                reg_write(reg_dest, result)

    elif instruction[:5] == '00011':
        # Subtract
        reg_dest = instruction[5:8]
        reg_a = instruction[10:13]
        reg_b = instruction[13:16]
        reg_a_data = reg_read(reg_a)
        reg_b_data = reg_read(reg_b)
        max_bits = max(len(reg_a_data), len(reg_b_data))
        reg_a_data = reg_a_data.zfill(max_bits)
        reg_b_data = reg_b_data.zfill(max_bits)
        result = bin((int(reg_a_data, 2) - int(reg_b_data, 2)) &
                     ((1 << max_bits) - 1))[2:].zfill(max_bits)
        reg_write(reg_dest, result)
        print(f"Subtracted register {int(reg_a, 2)} valued {int(reg_a_data, 2)} and register {int(reg_b, 2)} valued {int(reg_b_data, 2)} resulting {int(reg_a_data, 2) - int(reg_b_data, 2)} saving result in reg {int(reg_dest, 2)}")

    elif instruction[:5] == '00100':
        # Multiply
        reg_dest = instruction[5:8]
        flag_state = instruction[8:9]
        reg_a = instruction[10:13]
        reg_b = instruction[13:16]
        reg_a_data = reg_read(reg_a)
        reg_b_data = reg_read(reg_b)
        result = bin(int(reg_a_data, 2) *
                     int(reg_b_data, 2))[2:].zfill(reg_len)
        if len(result) == reg_len:
            reg_write(reg_dest, result)
            print(f"Multiplied register {int(reg_a, 2)} valued {int(reg_a_data, 2)} and register {int(reg_b, 2)} valued {int(reg_b_data, 2)} resulting {int(reg_a_data, 2) * int(reg_b_data, 2)} saving result in reg {int(reg_dest, 2)}")
        else:
            if flag_state == '1':
                flag = result[:1]
                result = result[1:]
                reg_write(reg_dest, result)
                print(f"Multiplied register {int(reg_a, 2)} valued {int(reg_a_data, 2)} and register {int(reg_b, 2)} valued {int(reg_b_data, 2)} resulting {int(reg_a_data, 2) * int(reg_b_data, 2)} which is too large, saving
                 {int(reg_dest, 2)}") 
            elif flag_state == '0':
                result = result[1:]
                reg_write(reg_dest, result)
    elif instruction[:5] == '00101':
        # Divide
        reg_dest = instruction[5:8]
        remainder_state = instruction[8:10]
        reg_a = instruction[10:13]
        reg_b = instruction[13:16]
        reg_a_data = reg_read(reg_a)
        reg_b_data = reg_read(reg_b)

        whole_number, whole_remainder = divmod(
            int(reg_a_data, 2), int(reg_b_data, 2))
        whole_number_binary = bin(whole_number)[2:].zfill(reg_len)

        remainder = float(whole_remainder) / float(int(reg_b_data, 2))
        remainder_binary = ""
        for _ in range(reg_len):
            remainder *= 2
            binary_digit = int(remainder)
            remainder_binary += str(binary_digit)
            remainder -= binary_digit

        whole_remainder_binary = bin(whole_number)[2:].zfill(reg_len)

        def next_register(reg_id):
            if reg_id == '111':
                return '000'
            else:
                dec_id = int(reg_id, 2)
                dec_id += 1
                return bin(dec_id)[2:].zfill(3)

        reg_write(reg_dest, whole_number_binary)
        reg_dest = next_register(reg_dest)

        if remainder_state == '00':
            # no remainder
            break
        elif remainder_state == '01':
            # set the next register to whole remainder
            reg_write(reg_dest, whole_remainder_binary)
            break
        elif remainder_state == '10':
            # set the next register to decimal segment
            reg_write(reg_dest, remainder_binary)
            break
        elif remainder_state == '11':
            # set flag to 1
            if remainder_binary != '00000000':
                flag = 1
            else:
                break
            break
    elif instruction[:5] == '00110':
        # Square
        reg_dest = instruction[5:8]
        flag_state = instruction[8:9]
        reg_a = instruction[10:13]
        reg_b = instruction[13:16]
        reg_a_data = reg_read(reg_a)
        reg_b_data = reg_read(reg_b)

        squared_number_dec = int(reg_a_data, 2) ** int(reg_b_data, 2)
        squared_number_bin = '00000000'

        if squared_number_dec > 255:
            squared_number_bin = '00000000'
            if flag_state == 1:
                flag = 1
        else:
            squared_number_bin = bin(squared_number_dec)[
                2:].zfill(8)

    elif instruction[:5] == '11010':
        # Load Immediate
        reg_dest = instruction[5:8]
        data = instruction[8:16]
        reg_write(reg_dest, data)
    else:
        print('unavailable instruction')
