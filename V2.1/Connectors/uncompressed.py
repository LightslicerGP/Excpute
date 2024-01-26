file = "ExampleInstruction.txt"


def opcode_table(opcode):
    opcode_dict = {
        'HLT': '00001',
        'ADD': '00010',
        'SUB': '00011',
        'MLT': '00100',
        'DVS': '00101',
        'SQA': '00110',
        'SQR': '00111',
        'FTR': '01000',
        'ORR': '01001',
        'AND': '01010',
        'XOR': '01011',
        'INV': '01100',
        'INC': '01101',
        'DEC': '01110',
        'RBS': '01111',
        'LBS': '10000',
        'EQL': '10001',
        'NEQ': '10010',
        'GRT': '10011',
        'LST': '10100',
        'GTE': '10101',
        'LTE': '10110',
        'SPD': '10111',
        'PTI': '11000',
        'PTO': '11001',
        'LDI': '11010',
        'LOD': '11011',
        'STR': '11100',
        'JMP': '11101',
        'JIZ': '11110',
        'RST': '11111'
    }
    return opcode_dict.get(opcode, '00000')


def num2bin(num, digits=3):
    prebinary = bin(int(num))[2:]

    if len(prebinary) > digits:
        raise ValueError(
            f"Binary representation exceeds {digits} digits: {prebinary}, from converting {num}")

    binary = prebinary.zfill(digits)
    return binary


with open(file, 'r') as f:
    instruction_set = f.read().split('\n')

    split_instructions = []

    for instruction in instruction_set:
        instruction_line = instruction.split()
        print(instruction_line)

        if not instruction_line:
            print('error ig idk')
            continue
        opcode = instruction_line[0]
        opcode_binary = opcode_table(opcode)
        split_instructions.append(opcode_binary)

        if instruction_line[0] in ['NOP', 'HLT']:
            split_instructions.append('00000000000')

        if instruction_line[0] in ['ADD', 'MLT', 'SQA']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            flag = num2bin(instruction_line[2], 1)
            split_instructions.append(flag)

            split_instructions.append('0')

            reg_a = num2bin(instruction_line[3])
            split_instructions.append(reg_a)

            reg_b = num2bin(instruction_line[4])
            split_instructions.append(reg_b)

        elif instruction_line[0] in ['SUB', 'DVS', 'SQR', 'ORR', 'AND', 'XOR']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            split_instructions.append('00')

            reg_a = num2bin(instruction_line[2])
            split_instructions.append(reg_a)

            reg_b = num2bin(instruction_line[3])
            split_instructions.append(reg_b)

        elif instruction_line[0] in ['FTR', 'INC']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            flag = num2bin(instruction_line[2], 1)
            split_instructions.append(flag)

            split_instructions.append('0')

            reg_a = num2bin(instruction_line[3])
            split_instructions.append(reg_a)

            split_instructions.append('000')

        elif instruction_line[0] in ['INV', 'DEC']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            split_instructions.append('00')

            reg_a = num2bin(instruction_line[2])
            split_instructions.append(reg_a)

            split_instructions.append('000')

        elif instruction_line[0] in ['LDI']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            location_id = num2bin(instruction_line[2], 8)
            split_instructions.append(location_id)

        elif instruction_line[0] in ['RBS', 'LBS']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            d_or_f = num2bin(instruction_line[2], 2)
            split_instructions.append(d_or_f)

            reg_a = num2bin(instruction_line[3])
            split_instructions.append(reg_a)

            split_instructions.append('000')

        elif instruction_line[0] in ['EQL', 'NEQ', 'GRT', 'LST', 'GTE', 'LTE']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            d_or_f = num2bin(instruction_line[2], 2)
            split_instructions.append(d_or_f)

            reg_a = num2bin(instruction_line[3])
            split_instructions.append(reg_a)

            reg_b = num2bin(instruction_line[4])
            split_instructions.append(reg_b)

        elif instruction_line[0] in ['SPD', 'PTI', 'PTO']:
            mode = num2bin(instruction_line[1])
            split_instructions.append(mode)

            data = num2bin(instruction_line[2], 8)
            split_instructions.append(data)

        elif instruction_line[0] in ['LOD']:
            reg_dest = num2bin(instruction_line[1])
            split_instructions.append(reg_dest)

            split_instructions.append('00000000')

        elif instruction_line[0] in ['STR']:
            split_instructions.append('00000')

            reg_a = num2bin(instruction_line[1])
            split_instructions.append(reg_a)

            split_instructions.append('000')

        elif instruction_line[0] in ['JMP', 'JIZ']:
            split_instructions.append('00000')

            reg_a = num2bin(instruction_line[1])
            split_instructions.append(reg_a, 6)

        elif instruction_line[0] in ['RST']:
            split_instructions.append('000')

            reg_a = num2bin(instruction_line[1])
            split_instructions.append(reg_a, 2)

            split_instructions.append('000000')

    binary_instruction = ''.join(split_instructions)

print('\n', split_instructions)
print('\n', binary_instruction)
