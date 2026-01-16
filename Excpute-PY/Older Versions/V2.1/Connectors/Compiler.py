file = "Connectors/ExampleInstruction.asm"


def opcode_table(opcode):
    opcode_dict = {
        "HLT": "00001",
        "ADD": "00010",
        "SUB": "00011",
        "MLT": "00100",
        "DVS": "00101",
        "SQA": "00110",
        "SQR": "00111",
        "FTR": "01000",
        "ORR": "01001",
        "AND": "01010",
        "XOR": "01011",
        "INV": "01100",
        "INC": "01101",
        "DEC": "01110",
        "RBS": "01111",
        "LBS": "10000",
        "EQL": "10001",
        "NEQ": "10010",
        "GRT": "10011",
        "LST": "10100",
        "GTE": "10101",
        "LTE": "10110",
        "SPD": "10111",
        "PTI": "11000",
        "PTO": "11001",
        "LDI": "11010",
        "LOD": "11011",
        "STR": "11100",
        "JMP": "11101",
        "JIS": "11110",
        "RST": "11111",
    }
    return opcode_dict.get(opcode, "00000")


def num2bin(num, digits=3):
    prebinary = bin(int(num))[2:]
    if len(prebinary) > digits:
        raise ValueError(
            f"Error from converting '{num}', Binary representation exceeds {digits} digits: {len(prebinary)} digits required."
        )
    binary = prebinary.zfill(digits)
    return binary


with open(file, "r") as f:
    instruction_set = f.read().split("\n")
    split_instructions = []
    for instruction in instruction_set:
        instruction_line = instruction.split()
        print(instruction_line)
        if not instruction_line:
            print("error ig idk")
            continue
        opcode = instruction_line[0]
        opcode_binary = opcode_table(opcode)
        split_instructions.append(opcode_binary)
        if instruction_line[0] in ["NOP", "HLT"]:
            split_instructions.append("00000000000")
        if instruction_line[0] in ["ADD"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[3]))
            except IndexError:
                split_instructions.append("010")
            # Set Flag
            try:
                split_instructions.append(num2bin(instruction_line[4], 1))
            except IndexError:
                split_instructions.append("0")
            # Carry Flag
            try:
                split_instructions.append(num2bin(instruction_line[5], 1))
            except IndexError:
                split_instructions.append("0")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            # Reg B
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("001")
        elif instruction_line[0] in ["SUB", "ORR", "AND", "XOR"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[3]))
            except IndexError:
                split_instructions.append("010")
            split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            # Reg B
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("001")
        elif instruction_line[0] in ["MLT", "SQA", "FTR"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[3]))
            except IndexError:
                split_instructions.append("010")
            # Set Flag
            try:
                split_instructions.append(num2bin(instruction_line[4], 1))
            except IndexError:
                split_instructions.append("0")
            split_instructions.append("0")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            # Reg B
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("001")
        elif instruction_line[0] in ["DVS", "SQR"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[3]))
            except IndexError:
                split_instructions.append("010")
            # Remainder
            try:
                split_instructions.append(num2bin(instruction_line[4], 2))
            except IndexError:
                split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            # Reg B
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("001")
        elif instruction_line[0] in ["INV", "DEC"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("010")
            split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["INC"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("010")
            # Set Flag
            try:
                split_instructions.append(num2bin(instruction_line[2], 1))
            except IndexError:
                split_instructions.append("0")
            split_instructions.append("0")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["RBS", "LBS"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("010")
            # Data Flag
            try:
                split_instructions.append(num2bin(instruction_line[3], 2))
            except IndexError:
                split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["EQL", "NEQ", "GRT", "LST", "GTE", "LTE"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[3]))
            except IndexError:
                split_instructions.append("010")
            # Data Flag
            try:
                split_instructions.append(num2bin(instruction_line[4], 2))
            except IndexError:
                split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            # Reg b
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("001")
        elif instruction_line[0] in ["SPD"]:
            # Property
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1], 2))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["PTI"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("100")
            # Port ID
            try:
                split_instructions.append(num2bin(instruction_line[1], 8))
            except IndexError:
                split_instructions.append("00000000")
        elif instruction_line[0] in ["PTO", "LDI"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("100")
            # Port ID
            try:
                split_instructions.append(num2bin(instruction_line[2], 8))
            except IndexError:
                split_instructions.append("00000000")
        elif instruction_line[0] in ["LOD"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("010")
            split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["STR"]:
            # Reg Dest
            try:
                split_instructions.append(num2bin(instruction_line[1]))
            except IndexError:
                split_instructions.append("010")
            split_instructions.append("00")
            # Reg A
            try:
                split_instructions.append(num2bin(instruction_line[2]))
            except IndexError:
                split_instructions.append("000")
            split_instructions.append("000")
        elif instruction_line[0] in ["JMP", "JIS"]:
            split_instructions.append("000")
            # Jump Adress
            try:
                split_instructions.append(num2bin(instruction_line[1], 8))
            except IndexError:
                split_instructions.append("00000000")
        elif instruction_line[0] in ["RST"]:
            split_instructions.append("000")
            # Jump Adress
            try:
                split_instructions.append(num2bin(instruction_line[1], 2))
            except IndexError:
                split_instructions.append("00")
            split_instructions.append("000000")
    binary_string_instruction = "".join(split_instructions)

print("split_instructions:", split_instructions)
print("binary_split_instructions:", binary_string_instruction)

binary_instructions = []

for instruction in split_instructions:
    binary_instructions.append(int(instruction, 2))

print(
    "\n",
    len(binary_string_instruction),
    "bits,",
    int(len(binary_string_instruction) / 8),
    "bytes,",
    int(len(binary_string_instruction) / 16),
    "instructions",
)

with open("binary instruction", "w") as output_file:
    output_file.write(binary_string_instruction)

with open("Binary Instruction.bin", "wb") as f:
    bytes_list = []

    for i in range(0, len(binary_string_instruction), 8):
        byte = binary_string_instruction[i : i + 8]
        bytes_list.append(int(byte, 2))

    print("bytes_list:", bytes_list)

    f.write(bytes(bytes_list))

print(f"Binary instructions written to myprogram.bin")
