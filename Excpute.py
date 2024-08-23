# import Operations
import threading
import pygame
import re
import Display
import Port
import RAM

registers = [0] * 8


def display_start():
    Display.start()


threading.Thread(target=display_start, daemon=True).start()
debug = False
print_registers = False


def reg_read(id: int, signed: bool = True):
    value = registers[id]
    if not signed:  # 0 to 255
        return value
        # -128 to 127
    if value > 127:  # when sig bit is 1, meaning negative
        return -(256 - value)
    else:  # when sig bit is 0, meaning positive
        return value


def reg_write(id: int, new_data: int, signed: bool = True):
    if (
        signed and -128 <= new_data < 0
    ):  # converts the negative number to unsigned number
        registers[id] = 256 + new_data
    elif (not signed and 0 <= new_data <= 255) or (
        signed and 0 <= new_data <= 127
    ):  # sb doesnt matter, write number
        registers[id] = new_data
    else:
        raise OverflowError(f"Cannot write {new_data} to register {id}")


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


def next_instruction():
    if instruction_address == 255:
        reg_write(7, 0, False)
    else:
        reg_write(7, instruction_address + 1, False)


def hlt_op():
    if debug:
        print(f"{instruction_address}: Halt Operation")
    exit()


def add_op(regA, regB, regDest, SetFlag, CarryFlag):
    if debug:
        print(f"{instruction_address}: Addition")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    if CarryFlag == 1:
        result = A + B + flag_read("carry")
    else:
        result = A + B

    if result > 127:
        result = result - 256
    elif result < -128:
        if SetFlag == 1:
            flag_set("carry", 1)
        result = result + 256
    reg_write(regDest, result)
    next_instruction()


def sub_op(regA, regB, regDest, SetFlag):
    if debug:
        print(f"{instruction_address}: Subtraction")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    result = A - B

    if result > 127:
        result = result - 256
    elif result < -128:
        if SetFlag == 1:
            flag_set("carry", 1)
        result = result + 256

    reg_write(regDest, result)
    next_instruction()


def mul_op(regA, regB, regDest, SetFlag):
    if debug:
        print(f"{instruction_address}: Multiplication")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    print("do later, too complicated so itll take too long to make rn")
    next_instruction()


def dvs_op(regA, regB, regDest):
    if debug:
        print(f"{instruction_address}: Division")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    print("do later, too complicated so itll take too long to make rn")
    next_instruction()


def sqa_op(regA, regB, regDest, SetFlag):
    if debug:
        print(f"{instruction_address}: Square")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    print("do later, too complicated so itll take too long to make rn")
    next_instruction()


def sqr_op(regA, regB, regDest):
    if debug:
        print(f"{instruction_address}: Square root")
    A = reg_read(regA, True)
    B = reg_read(regB, True)

    print("do later, too complicated so itll take too long to make rn")
    next_instruction()


def orr_op(regA, regB, regDest):
    if debug:
        print(f"{instruction_address}: Or")
    A = reg_read(regA, False)  # THIS IS FALSE because
    B = reg_read(regB, False)  # its not math, just logic
    result = A | B
    reg_write(regDest, result, False)
    next_instruction()


def and_op(regA, regB, regDest):
    if debug:
        print(f"{instruction_address}: And")
    A = reg_read(regA, False)  # THIS IS FALSE because
    B = reg_read(regB, False)  # its not math, just logic
    result = A & B
    reg_write(regDest, result, False)
    next_instruction()


def xor_op(regA, regB, regDest):
    if debug:
        print(f"{instruction_address}: Xor")
    A = reg_read(regA, False)  # THIS IS FALSE because
    B = reg_read(regB, False)  # its not math, just logic
    result = A ^ B
    reg_write(regDest, result, False)
    next_instruction()


def inv_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Invert")
    A = reg_read(regA, False)  # THIS IS FALSE because its not math, just logic
    result = A ^ 255
    reg_write(regDest, result, False)
    next_instruction()


def inc_op(regA, regDest, SetFlag):
    if debug:
        print(f"{instruction_address}: Increment")
    A = reg_read(regA, False)
    if A == 255:
        if SetFlag == 1:
            flag_set("carry", 1)
        result = 0
    else:
        result = A + 1
    reg_write(regDest, result, False)
    next_instruction()


def dec_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Decrement")
    A = reg_read(regA, False)
    if A == 0:
        result = 255
    else:
        result = A - 1
    reg_write(regDest, result, False)
    next_instruction()


def rsh_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Right shift")
    A = reg_read(regA, False)
    result = A >> 1
    reg_write(regDest, result, False)
    next_instruction()


def lsh_op(regA, regDest, SetFlag):
    if debug:
        print(f"{instruction_address}: Left shift")
    A = reg_read(regA, False)

    result = A << 1

    if result > 255:
        if SetFlag == 1:
            flag_set("carry", 1)
        result = result - 256
        
    reg_write(regDest, result, False)
    next_instruction()


def rbs_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Right barrel shift")
    A = reg_read(regA, False)

    result = (A >> 1) | (A << 7) & 255

    reg_write(regDest, result, False)

    next_instruction()


def lbs_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Left barrel shift")
    A = reg_read(regA, False)

    result = ((A << 1) | (A >> 7)) & 255

    reg_write(regDest, result, False)

    next_instruction()


def cmp_op(regA, regB):
    if debug:
        print(f"{instruction_address}: Compare")
    A = reg_read(regA, False)
    B = reg_read(regB, False)

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


def psh_op(regA):
    if debug:
        print(f"{instruction_address}: Push to stack")
    A = reg_read(regA, False)
    stack_pointer = reg_read(5, False)
    RAM.write(stack_pointer, A, False)  # writes to stack
    reg_write(5, reg_read(5, False) - 1, False)  # "increments" (decrements) pointer
    next_instruction()


def pop_op(regDest):
    if debug:
        print(f"{instruction_address}: Pop from stack")
    stack_pointer = reg_read(5, False)
    pointer_data = RAM.read(stack_pointer + 1, False)  # reads last pointer location
    reg_write(regDest, pointer_data, False)  # writes from stack
    reg_write(5, stack_pointer + 1, False)  # "decrements" (increments) pointer
    next_instruction()


def cal_op(jump_to):
    if debug:
        print(f"{instruction_address}: Call from stack")
    stack_pointer = reg_read(5, False)
    RAM.write(stack_pointer, instruction_address + 1, False)  # writes to stack
    reg_write(5, stack_pointer - 1, False)  # "increments" (decrements) pointer
    reg_write(7, jump_to, False)  # jumps to new instruction adress
    # instead of running next_instruction()


def rtn_op():
    if debug:
        print(f"{instruction_address}: Return from stack")
    stack_pointer = reg_read(5, False)
    pointer_data = RAM.read(stack_pointer + 1, False)  # reads last pointer location
    reg_write(5, stack_pointer + 1, False)  # "decrements" (increments) pointer
    # is this neccessary? - no RAM.write(stack_pointer + 1, 0, False)  # writes 0 to current pointer location
    reg_write(7, pointer_data, False)  # returns to the instruction adress


def cpy_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Copy")
    data = reg_read(regA)
    reg_write(regDest, data)
    next_instruction()


def ldi_op(address, number):
    if debug:
        print(f"{instruction_address}: Load immediate")
    reg_write(address, number)
    next_instruction()


def lod_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Load from memory")
    A = reg_read(regA)
    data = RAM.read(A)
    reg_write(regDest, data)
    next_instruction()


def str_op(regA, regDest):
    if debug:
        print(f"{instruction_address}: Store to memory")
    A = reg_read(regA)
    Destination = reg_read(regDest, False)
    RAM.write(Destination, A)
    next_instruction()


def pti_op(address, regDest):
    if debug:
        print(f"{instruction_address}: Port input")
    data = Port.read(address)
    reg_write(regDest, data)
    next_instruction()


def pto_op(regA, address):
    if debug:
        print(f"{instruction_address}: Port output")
    Port.write(regA, address)
    next_instruction()


def jmp_op(address):
    if debug:
        print(f"{instruction_address}: Jump to instruction")
    reg_write(7, address, False)


def jiz_op(regA, address):
    if debug:
        print(f"{instruction_address}: Jump if zero")
    A = reg_read(regA)
    if A == 0:
        reg_write(7, address, False)
    else:
        next_instruction()


def spd_op(regA, property):
    if debug:
        print(f"{instruction_address}: Set pixel data")
    A = reg_read(regA, False)

    property_mapping = {0: 249, 1: 250, 2: 251, 3: 252, 4: 253}

    if property in property_mapping:  # r, g, b, x, y
        RAM.write(property_mapping[property], A, False)
    elif property == 5:
        RAM.write(254, 1)  # set
        Display.refresh()
    elif property == 6:
        RAM.write(254, 2)  # reset
        Display.refresh()
    elif property == 7:
        RAM.write(254, 3)  # fill
        Display.refresh()

    next_instruction()


instruction_address = reg_read(7, False)
reg_write(7, 0, False)  # set instruction address
reg_write(5, 248, False)  # set stack address


instructions = {
    "NOP": lambda: None,
    "HLT": lambda: hlt_op(),
    "ADD": lambda ra, rb, rd, sf=1, cf=0: add_op(ra, rb, rd, sf, cf),
    "SUB": lambda ra, rb, rd, sf=1: sub_op(ra, rb, rd, sf),
    "MUL": lambda ra, rb, rd, sf=2: mul_op(ra, rb, rd, sf),
    "DVS": lambda ra, rb, rd: dvs_op(ra, rb, rd),
    "SQA": lambda ra, rb, rd, sf=1: sqa_op(ra, rb, rd, sf),
    "SQR": lambda ra, rb, rd: sqr_op(ra, rb, rd),
    "ORR": lambda ra, rb, rd: orr_op(ra, rb, rd),
    "AND": lambda ra, rb, rd: and_op(ra, rb, rd),
    "XOR": lambda ra, rb, rd: xor_op(ra, rb, rd),
    "INV": lambda ra, rd: inv_op(ra, rd),
    "INC": lambda ra, rd, sf=1: inc_op(ra, rd, sf),
    "DEC": lambda ra, rd: dec_op(ra, rd),
    "RSH": lambda ra, rd: rsh_op(ra, rd),
    "LSH": lambda ra, rd, sf=1: lsh_op(ra, rd, sf),
    "RBS": lambda ra, rd: rbs_op(ra, rd),
    "LBS": lambda ra, rd: lbs_op(ra, rd),
    "CMP": lambda ra, rb: cmp_op(ra, rb),
    "PSH": lambda ra: psh_op(ra),
    "POP": lambda rd: pop_op(rd),
    "CAL": lambda ad: cal_op(ad),
    "RTN": lambda: rtn_op(),
    "CPY": lambda ra, rd: cpy_op(ra, rd),
    "LDI": lambda ad, nu: ldi_op(ad, nu),
    "LOD": lambda ra, rd: lod_op(ra, rd),
    "STR": lambda ra, rd: str_op(ra, rd),
    "PTI": lambda ad, rd: pti_op(ad, rd),
    "PTO": lambda ra, ad: pto_op(ra, ad),
    "JMP": lambda ad: jmp_op(ad),
    "JIZ": lambda ra, ad: jiz_op(ra, ad),
    "SPD": lambda ra, pr: spd_op(ra, pr),
}

def get_instructions(file):
    with open(file, "r") as instruction_file:
        lines = instruction_file.readlines()
    instruction_array = [
        tuple(
            int(item) if re.match(r"^-?\d+$", item) else item
            for item in line.strip().split()
        )
        for line in lines
    ]
    return instruction_array

program = get_instructions("Instructions Compiled")

if debug:
    print(program)

while instruction_address < 256:
    try:
        instruction = program[instruction_address]
    except IndexError:
        print("Ran out of instructions, halted automatically")
        if debug:
            print("Instruction address:", instruction_address)
        exit()
    op = instruction[0].upper()
    args = instruction[1:]

    instructions[op](*args)
    if debug or print_registers:
        print(registers)

    instruction_address = reg_read(7, False)


events = pygame.event.get()
for event in events:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_0:
            exit()
