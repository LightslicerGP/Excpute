import RAM
import Compiler


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


def flag_read(flag: str):
    flag_bits = {"carry": -1, "zero": -2, "parity": -3, "negative": -4}
    flag_byte = list(bin(reg_read(6, False))[2:].zfill(8))

    if flag in flag_bits:
        return int(flag_byte[flag_bits[flag]])
    else:
        raise ValueError("Flag must be carry, zero, parity, overflow, or negative")


with open("assembled instruction", "r") as file:
    instructions = [
        ([int(x) if x.lstrip("-").isdigit() else x for x in line.split()])
        for line in file
    ]


# setup registers and ram

Compiler.reset()
print("---------------")
# kinda unneccessary to have the first be false but whatever
reg_write(7, 0, False)  # set instruction address
reg_write(5, 248, False)  # set stack adress

instruction_address = reg_read(7, False)


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
        print(f"{instruction_address}: No Operation")
        next_instruction()
    elif instruction_line[0] == "HLT":
        print(f"{instruction_address}: Halt Operation")
        exit()
    elif instruction_line[0] == "ADD":
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
        print(f"{instruction_address}: Multiplication")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "DVS":
        print(f"{instruction_address}: Division")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "SQA":
        print(f"{instruction_address}: Square")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "SQR":
        print(f"{instruction_address}: Square root")
        A = reg_read(instruction_line[1], True)
        B = reg_read(instruction_line[2], True)
        Destination = instruction_line[3]

        print("do later, too complicated so itll take too long to make rn")
        next_instruction()
    elif instruction_line[0] == "ORR":
        print(f"{instruction_address}: Or")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A | B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "AND":
        print(f"{instruction_address}: And")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A & B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "XOR":
        print(f"{instruction_address}: Xor")
        A = reg_read(instruction_line[1], False)  # THIS IS FALSE because
        B = reg_read(instruction_line[2], False)  # its not math, just logic
        Destination = instruction_line[3]
        result = A & B
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "INV":
        print(f"{instruction_address}: Invert")
        A = reg_read(
            instruction_line[1], False
        )  # THIS IS FALSE because its not math, just logic
        Destination = instruction_line[2]
        result = A ^ 255
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "INC":
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
        print(f"{instruction_address}: Right shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]
        result = A >> 1
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "LSH":
        print(f"{instruction_address}: Right shift")
        A = reg_read(instruction_line[1], False)
        Destination = instruction_line[2]
        try:
            SetFlag = instruction_line[3]
        except IndexError:
            SetFlag = 1

        print(bin(A))
        if (A << 1) > 255:
            if SetFlag == 1:
                flag_set("carry", 1)
            # trim left 3 and then convert to number again? idk
            print(bin(A << 1))
        else:
            result = A << 1
        reg_write(Destination, result, False)
        next_instruction()
    elif instruction_line[0] == "CAL":
        jump_to = instruction_line[1]
        print(f"{instruction_address}: Call from stack")
        RAM.write(reg_read(5, False), instruction_address + 1, False)  # writes to stack
        reg_write(5, reg_read(5, False) - 1, False)  # "increments" (decrements) pointer
        reg_write(7, jump_to, False)  # writes register 7 manually
        # instead of running next_instruction()
    elif instruction_line[0] == "RTN":
        print(f"{instruction_address}: Return from stack")
        stack_pointer = reg_read(5, False)
        pointer_data = RAM.read(stack_pointer + 1, False)
        reg_write(5, reg_read(5, False) + 1, False)
        reg_write(7, pointer_data, False)
    elif instruction_line[0] == "LDI":
        print(f"{instruction_address}: Load Immediate")
        Register = instruction_line[1]
        Data = instruction_line[2]
        reg_write(Register, Data)
        next_instruction()
    else:
        print(f"instruction {instruction_line[0]} not programmed yet")
        next_instruction()

    instruction_address = reg_read(7, False)
