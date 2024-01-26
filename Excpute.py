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


stack_pointer = 0
def push(data: int, signed: bool = True):
    print("stack pointer is currently at:", stack_pointer)
    byte_adress = -stack_pointer + 248
    reg_write(byte_adress, data, signed)
    stack_pointer = stack_pointer + 1
    print("after push, the stack pointer is at:", stack_pointer)


with open("assembled instruction", "r") as file:
    instructions = [
        ([int(x) if x.isdigit() else x for x in line.split()]) for line in file
    ]

reg_write(7, 0, False)
instruction_address = reg_read(7, False)

while instruction_address in range(256):
    instruction_line = instructions[instruction_address]

    def next_instruction():
        if instruction_address == 255:
            reg_write(7, 0, False)
        else:
            reg_write(7, instruction_address + 1, False)

    if instruction_line[0] == "NOP":
        print("No Operation")
        next_instruction()
    elif instruction_line[0] == "HLT":
        print("Halt Operation")
        raise ValueError("CPU Halted")
    elif instruction_line[0] == "ADD":
        print("Addition")
        A = instruction_line[1]
        B = instruction_line[2]
        Destination = instruction_line[3]
        reg_write(Destination, A + B)
        next_instruction()
    elif instruction_line[0] == "SUB":
        print("Addition")
        A = instruction_line[1]
        B = instruction_line[2]
        Destination = instruction_line[3]
        reg_write(Destination, A - B)
        next_instruction()
    elif instruction_line[0] == "CAL":
        push(reg_read(7, False) + 1, False)
    elif instruction_line[0] == "LDI":
        print("Load Immediate")
        Data = instruction_line[1]
        Register = instruction_line[2]
        reg_write(Register, Data)
        next_instruction()
    else:
        print(f"instruction {instruction_line[0]} not programmed yet")

    instruction_address = reg_read(7, False)
