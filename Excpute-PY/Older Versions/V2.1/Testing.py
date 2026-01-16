import json

"1/13/24, im going back to before raw binary data, and into using a json file for registers"

A = 0b0111
B = 0b1111
C = "010"

def bin2num(bin_str:str):
    try:
        print(f"converted {bin_str} to {int(bin_str, 2)}")
        return int(bin_str, 2)
    except ValueError:
        print(f"Invalid binary string: {bin_str}")
        return None

print(bin((A - B).to_bytes(2, byteorder="big", signed=True)[0]))
print(int.from_bytes((A - B).to_bytes(2, byteorder="big", signed=True)))

binary_string = "00000010"
shifted_result = format(int(binary_string, 2) >> 1, "08b")

print(shifted_result)
print(bin2num(C))

"""
okat
idea
only way to get around this
is to have it as a true number
then convert it using a custom converter, checking to see if its between -128 and 255
and then take it, consider the significant bit, and then send it back as a binary number integer
-me 11/9/23
bin_num = -0b1111111
print("bin_num:", ~bin_num + 1)


def reg_write(id, data: str):
    with open("Registers.json", "r") as register_file:
        registers = json.load(register_file)
    registers[id] = data
    with open("Registers.json", "w") as register_file:
        json.dump(registers, register_file, indent=4)


def reg_read(id):
    with open("Registers.bin", "rb") as f:
        return f.read()[id]


def switch_type(input, bits=8):
    print("input given:", input)
    print("type:", type(input))
    if isinstance(input, int):
        print("switching integer to string")
        if 0 <= input <= 255:
            print("number is between 0 and 255")
            print(
                bin(input)[2:].zfill(bits),
                "type:",
                type(bin(input)[2:].zfill(bits)),
            )
            return bin(input)[2:].zfill(bits)
        elif -128 <= input < 0:
            print("number is between -128 and 0")
            print("stright to bin:", bin(input))
            return bin(~(input + 1))[2:].zfill(bits)
        else:
            print("error")
    elif isinstance(input, str):
        print("string:", input)


reg_write(7, bin_num)
print(switch_type(bin_num))



instruction = '0001001000000001'

with open("Registers.bin", "wb") as f:
    print("writing register file", f.write(bytearray([0] * 8)))
with open("RAM.bin", "wb") as f:
    print("writing RAM file", f.write(bytearray([0] * 256)))


def reg_read(id):
    with open("Registers.bin", "rb") as f:
        data = f.read()
        index = int(id)
        if index < len(data):
            print("register read returns:", data[index])
            return(data[index])
        else:
            print("Index is out of range")

def reg_write(byte_index, new_byte):
    with open("Registers.bin", "rb") as file:
        data = bytearray(file.read())
        data[byte_index] = new_byte

    with open("Registers.bin", "wb") as file:
        file.write(data)

reg_write(0, 0b00000001)
reg_write(1, 0b00000010)

# ADDITION
reg_dest = instruction[5:8]
flag_state = instruction[8:9]
carry_state = instruction[9:10]
reg_a = instruction[10:13]
reg_b = instruction[13:16]
reg_a_data = reg_read(reg_a)
reg_b_data = reg_read(reg_b)
print("registers reading shows", reg_a_data, reg_b_data)
print("adding registers", reg_b_data + reg_a_data)





import json
instructionlist = "binary instruction"
instructionlist_bin = "Binary Instruction.bin"


def bin2num(bin_str):
    try:
        return int(bin_str, 2)
    except ValueError:
        print(f"Invalid binary string: {bin_str}")
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




reg_a_data = '11111111'
reg_b_data = '00000011'
flag_state = 0

squared_number_dec = int(reg_a_data, 2) ** int(reg_b_data, 2)
squared_number_bin = '00000000'
flag = 0

if squared_number_dec > 255:
    squared_number_bin = '00000000'
    if flag_state == 1:
        flag = 1

else:
    squared_number_bin = bin(squared_number_dec)[
        2:].zfill(8)  # trim to right 3


print(squared_number_dec, squared_number_bin, flag)



whole_number, whole_remainder = divmod(int(reg_a_data, 2), int(reg_b_data, 2))
whole_number_binary = bin(whole_number)[2:].zfill(8)

remainder = float(whole_remainder) / float(int(reg_b_data, 2))
remainder_binary = ""
for _ in range(8):
    remainder *= 2
    binary_digit = int(remainder)
    remainder_binary += str(binary_digit)
    remainder -= binary_digit

whole_remainder_binary = bin(whole_number)[2:].zfill(8)

print("Whole Number (Binary): " + whole_number_binary)
print("Non-Decimal Result (Binary): " + whole_remainder_binary)
print("Remainder Result (Binary): " + remainder_binary)



def next_register(reg_id):
    if reg_id == '111':
        return '000'
    else:
        dec_id = int(reg_id, 2)
        dec_id += 1
        return bin(dec_id)[2:].zfill(3)

register_example = '111'
print("current register: ", register_example,
      ", next register", next_register(register_example))





def fraction_to_binary(numerator, denominator):

    if denominator == 0:
        raise ValueError("Denominator cannot be zero.")

    # Get the greatest common divisor of the numerator and denominator.
    gcd = math.gcd(numerator, denominator)

    # Divide the numerator and denominator by the greatest common divisor.
    numerator //= gcd
    denominator //= gcd

    # Convert the numerator and denominator to binary.
    binary_numerator = bin(numerator)[2:]
    binary_denominator = bin(denominator)[2:]

    # Pad the binary representation of the numerator with zeros to the same length as the binary representation of the denominator.
    binary_numerator = binary_numerator.zfill(8)

    # Return the binary representation of the fraction.
    return binary_numerator + binary_denominator


print(fraction_to_binary(whole_remainder, int(reg_b_data, 2)))

print(divmod(int(reg_a, 2), int(reg_b, 2)))





flag = '0'

if len(result) <= 8:
    print(result.zfill(8))
else:
    flag = '1'
    result = result[1:]
    print(result, flag)

string = 'abcdefghijklmnopqrstuvwxyz'
print(string[:5])
print(string[5:13])


def bin2num(bin):
    return int(bin, 2)


def num2bin(num):
    return bin(int(num))


print(bin2num('111111111111'))

print(num2bin('127'))
"""
