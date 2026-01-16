import threading
import time
import Compiler
import RAM
import Port
import Display
# import numba

# numba.njit(cache = True)

def reg_read(id: int, signed: bool = True):
    with open("Registers.bin", "rb") as f:
        value = f.read()[id]
    if not signed:  # 0 to 255
        return value
        # -128 to 127
    if value > 127:  # when sig bit is 1, meaning negative
        return -(256 - value)
    else:  # when sig bit is 0, meaning positive
        return value


def reg_write(id: int, new_data: int, signed: bool = True):
    with open("Registers.bin", "rb") as file:
        data = bytearray(file.read())
        if (
            signed and -128 <= new_data < 0
        ):  # converts the negative number to unsigned number
            data[id] = 256 + new_data
        elif (not signed and 0 <= new_data <= 255) or (
            signed and 0 <= new_data <= 127
        ):  # sb doesnt matter, write number
            data[id] = new_data
        else:
            raise OverflowError(f"Cannot write {new_data} to register {id}")

    with open("Registers.bin", "wb") as file:
        file.write(data)


def flag_read(flag: str):
    flag_bits = {"carry": -1, "zero": -2, "parity": -3, "negative": -4}
    flag_byte = list(bin(reg_read(6, False))[2:].zfill(8))

    if flag in flag_bits:
        return int(flag_byte[flag_bits[flag]])
    else:
        raise ValueError("Flag must be carry, zero, parity, overflow, or negative")


def flag_set(flag: str, sign: int):
    flag_bits = {"carry": -1, "zero": -2, "parity": -3, "negative": -4, "overflow": -5}

    if sign == 0 or sign == 1:
        flag_byte = list(bin(reg_read(6, False))[2:].zfill(8))

        if flag in flag_bits:
            flag_byte[flag_bits[flag]] = str(sign)
            updated_flag = int("".join(flag_byte), 2)
            reg_write(6, updated_flag, False)
        else:
            raise ValueError("Flag must be carry, zero, parity, overflow, or negative")

    else:
        raise ValueError("flag_write number must be 1 or 0")


with open("assembled instruction", "r") as file:
    instructions = [
        ([int(x) if x.lstrip("-").isdigit() else x for x in line.split()])
        for line in file
    ]


# setup registers, ram, and display

Compiler.reset()
print("---------------")
# kinda unneccessary to have the first be false but whatever
reg_write(7, 0, False)  # set instruction address
reg_write(5, 248, False)  # set stack address
instruction_address = reg_read(7, False)  # set instruction pointer
debug = False

def display_start():
    Display.start()
    
threading.Thread(target=display_start, daemon=True).start()

time.sleep(2)

while instruction_address in range(256):
    try:
        instruction_line = instructions[instruction_address]
    except IndexError:
        print("Ran out of instructions, halted automatically")
        exit()

    def next_instruction():
        if instruction_address == 255:
            reg_write(7, 0, False)
        else:
            reg_write(7, instruction_address + 1, False)

    if instruction_line[0] == "NOP":
        if debug:
            print(f"{instruction_address}: No Operation")
        next_instruction()
    elif instruction_line[0] == "HLT":
        if debug:
            print(f"{instruction_address}: Halt Operation")
        exit()
    elif instruction_line[0] == "ADD":
        if debug:
            print(f"{instruction_address}: Addition")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]
        try:
            SetFlag = instruction_line[4]
        except IndexError:
            SetFlag = 1
        try:
            CarryFlag = instruction_line[5]
        except IndexError:
            CarryFlag = 0

        if CarryFlag == 1:
            if flag_read("carry") == 1:
                result = A + B + 1
        else:
            result = A + B

        if not (-128 <= result <= 127):
            if SetFlag == 1:
                flag_set("carry", 1)
            result = int(bin(result)[3:], 2)
        reg_write(Destination, result)
        next_instruction()
    elif instruction_line[0] == "SUB":
        if debug:
            print(f"{instruction_address}: Subtraction")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]
        try:
            SetFlag = instruction_line[4]
        except IndexError:
            SetFlag = 1

        result = A - B

        if not (-128 <= result <= 127):
            if SetFlag == 1:
                flag_set("carry", 1)
            result = int(bin(256 + result)[2:], 2)

        reg_write(Destination, result)
        next_instruction()
    elif instruction_line[0] == "MUL":
        if debug:
            print(f"{instruction_address}: Multiplication")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "DVS":
        if debug:
            print(f"{instruction_address}: Division")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "SQA":
        if debug:
            print(f"{instruction_address}: Square")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "SQR":
        if debug:
            print(f"{instruction_address}: Square root")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "ORR":
        if debug:
            print(f"{instruction_address}: Or")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A | B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "AND":
        if debug:
            print(f"{instruction_address}: And")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A & B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "XOR":
        if debug:
            print(f"{instruction_address}: Xor")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A & B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "INV":
        if debug:
            print(f"{instruction_address}: Invert")
        A = reg_read(
            instruction_line[1], False
        )  # THIS IS FALSE because its not math, just logic
        Destination = instruction_line[2]
        result = A ^ 255
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "INC":
        if debug:
            print(f"{instruction_address}: Increment")
        A = reg_read(instruction_line[1])
        Destination = instruction_line[2]
        if A == 127:
            result = -128
        else:
            result = A + 1
        reg_write(Destination, result)
        next_instruction()
    elif instruction_line[0] == "DEC":
        if debug:
            print(f"{instruction_address}: Decrement")
        A = reg_read(instruction_line[1])
        Destination = instruction_line[2]
        if A == -128:
            result = 127
        else:
            result = A - 1
        reg_write(Destination, result)
        next_instruction()
    elif instruction_line[0] == "RSH":
        if debug:
            print(f"{instruction_address}: Right shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]
        result = A >> 1
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "LSH":
        if debug:
            print(f"{instruction_address}: Left shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]
        try:
            SetFlag = instruction_line[3]
        except IndexError:
            SetFlag = 1

        if (A << 1) > 255:
            if SetFlag == 1:
                flag_set("carry", 1)
            result = (A << 1) - 256
            reg_write(Destination, result, False)
        else:
            result = A << 1
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "RBS":
        if debug:
            print(f"{instruction_address}: Right barrel shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]

        result = (A >> 1) | (A << 7) & 255

        reg_write(Destination, result, False)

        next_instruction()
    elif instruction_line[0] == "LBS":
        if debug:
            print(f"{instruction_address}: Left barrel shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]

        result = ((A << 1) | (A >> 7)) & 255

        reg_write(Destination, result, False)

        next_instruction()
    elif instruction_line[0] == "CMP":
        if debug:
            print(f"{instruction_address}: Compare")
        A = reg_read(instruction_line[1], False)
        B = reg_read(instruction_line[2], False)

        result = B - A

        if result == 0:
            flag_set("zero", 1)
        else:
            flag_set("zero", 0)

        if result < 0:
            flag_set("negative", 1)
        else:
            flag_set("negative", 0)

        if B < A:
            flag_set("carry", 1)
        else:
            flag_set("carry", 0)

        next_instruction()
    elif instruction_line[0] == "PSH":
        if debug:
            print(f"{instruction_address}: Push to stack")
        A = reg_read(instruction_line[1], False)
        stack_pointer = reg_read(5, False)
        RAM.write(stack_pointer, A, False)  # writes to stack
        reg_write(5, reg_read(5, False) - 1, False)  # "increments" (decrements) pointer
        next_instruction()
    elif instruction_line[0] == "POP":
        if debug:
            print(f"{instruction_address}: Pop from stack")
        A = instruction_line[1]
        stack_pointer = reg_read(5, False)
        pointer_data = RAM.read(stack_pointer + 1, False)  # reads last pointer location
        reg_write(A, pointer_data, False)  # writes from stack
        reg_write(5, stack_pointer + 1, False)  # "decrements" (increments) pointer
        next_instruction()
    elif instruction_line[0] == "CAL":
        if debug:
            print(f"{instruction_address}: Call from stack")
        jump_to = instruction_line[1]
        stack_pointer = reg_read(5, False)
        RAM.write(stack_pointer, instruction_address + 1, False)  # writes to stack
        reg_write(5, stack_pointer - 1, False)  # "increments" (decrements) pointer
        reg_write(7, jump_to, False)  # jumps to new instruction adress
        # instead of running next_instruction()
    elif instruction_line[0] == "RTN":
        if debug:
            print(f"{instruction_address}: Return from stack")
        stack_pointer = reg_read(5, False)
        pointer_data = RAM.read(stack_pointer + 1, False)  # reads last pointer location
        reg_write(5, stack_pointer + 1, False)  # "decrements" (increments) pointer
        # is this neccessary? - no RAM.write(stack_pointer + 1, 0, False)  # writes 0 to current pointer location
        reg_write(7, pointer_data, False)  # returns to the instruction adress
    elif instruction_line[0] == "CPY":
        if debug:
            print(f"{instruction_address}: Copy")
        A = instruction_line[1]
        Destination = instruction_line[2]
        data = reg_read(A)
        reg_write(Destination, data)
        next_instruction()
    elif instruction_line[0] == "LDI":
        if debug:
            print(f"{instruction_address}: Load immediate")
        Register = instruction_line[1]
        Data = instruction_line[2]
        reg_write(Register, Data)
        next_instruction()
    elif instruction_line[0] == "LOD":
        if debug:
            print(f"{instruction_address}: Load from memory")
        A = reg_read(instruction_line[1])
        Destination = instruction_line[2]
        data = RAM.read(A)
        reg_write(Destination, data)
        next_instruction()
    elif instruction_line[0] == "STR":
        if debug:
            print(f"{instruction_address}: Store to memory")
        A = reg_read(instruction_line[1])
        Destination = reg_read(instruction_line[2], False)
        RAM.write(Destination, A)
        next_instruction()
    elif instruction_line[0] == "PTI":
        if debug:
            print(f"{instruction_address}: Port input")
        Address = instruction_line[1]
        Destination = instruction_line[2]
        data = Port.read(Address)
        reg_write(Destination, data)
        next_instruction()
    elif instruction_line[0] == "PTO":
        if debug:
            print(f"{instruction_address}: Port output")
        A = instruction_line[1]
        Address = instruction_line[2]
        Port.write(A, Address)
        next_instruction()
    elif instruction_line[0] == "JMP":
        if debug:
            print(f"{instruction_address}: Jump to instruction")
        Address = instruction_line[1]
        reg_write(7, Address, False)
    elif instruction_line[0] == "JIZ":
        if debug:
            print(f"{instruction_address}: Jump if zero")
        A = reg_read(instruction_line[1])
        Address = instruction_line[2]
        if A == 0:
            reg_write(7, Address, False)
        else:
            next_instruction()
    elif instruction_line[0] == "SPD":
        if debug:
            print(f"{instruction_address}: Set pixel data")
        A = reg_read(instruction_line[1], False)
        Property = instruction_line[2]

        property_mapping = {0: 249, 1: 250, 2: 251, 3: 252, 4: 253}

        if Property in property_mapping:  # r, g, b, x, y
            RAM.write(property_mapping[Property], A, False)
        elif Property == 5:
            RAM.write(254, 1)  # set
            Display.refresh()
        elif Property == 6:
            RAM.write(254, 2)  # reset
            Display.refresh()
        elif Property == 7:
            RAM.write(254, 3)  # fill
            Display.refresh()

        next_instruction()

    else:
        print(f"instruction {instruction_line[0]} not programmed yet or unavailable")
        next_instruction()

    instruction_address = reg_read(7, False)
