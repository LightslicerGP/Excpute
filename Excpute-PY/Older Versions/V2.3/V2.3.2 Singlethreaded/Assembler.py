import re

debug = False

# remove comments
print("removing comments") if debug else None
with open("Instructions Uncompiled", "r") as instruction_file:
    with open("Instructions Compiled", "w") as main_file:
        for line in instruction_file:
            line = line.split("#")[0].strip()
            main_file.write(line + "\n")

# remove extra lines
print("removing extra lines") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if line.strip():
            main_file.write(line)

# replace 0x and 0b with their decimal numbers
print("replacing 0x and 0b with their decimal numbers") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if "0x" in line:
            pattern = r"0x[0-9a-fA-F]+"
            line = re.sub(pattern, lambda x: str(int(x.group(0), 16)), line)
            main_file.write(line)
        elif "0b" in line:
            pattern = r"0b[01]+"
            line = re.sub(pattern, lambda x: str(int(x.group(0), 2)), line)
            main_file.write(line)
        else:
            main_file.write(line)

# keep track of const names, and the value, then delete the lines
(
    print("keeping track of const names, and the value, then deleting the lines")
    if debug
    else None
)
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    constants = {}
    for line in lines:
        if "=" in line:
            const_name, const_value = line.strip().split("=")
            const_name = const_name.strip()
            const_value = int(const_value.strip())
            constants[const_name] = const_value
            line = ""
        main_file.write(line)
    print("constants:", constants) if debug else None
    constants = dict(
        sorted(constants.items(), key=lambda item: len(item[0]), reverse=True)
    )  # so when replacing it checks longest first in case like "set" gets checked before "reset"
    print("constants sorted:", constants) if debug else None

# keep track of function names, and the line number, then delete the lines
(
    print(
        "keeping track of function names, and the line number, then deleting the lines"
    )
    if debug
    else None
)
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    line_number = 0
    jumps = {}
    for line in lines:
        if ":" in line:
            jump_name = line.split(":")[0]
            jumps[jump_name] = line_number
            line = ""
        else:
            line_number += 1
        main_file.write(line)
    print("jumps:", jumps) if debug else None
    jumps = dict(
        sorted(jumps.items(), key=lambda item: len(item[0]), reverse=True)
    )  # same reasoning as before
    print("jumps sorted:", jumps) if debug else None

#  Replace all constants names with their values
print("replacing all constants names with their values") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:

        if not line.lower().startswith(("cal", "jmp", "jiz")):
            for key, value in constants.items():
                line = line[:4] + line[4:].replace(key, str(value))

        elif line.lower().startswith("jiz"):
            split_line = line.split()
            for key, value in constants.items():
                split_line[1] = split_line[1].replace(key, str(value))
            line = f"{split_line[0]} {split_line[1]} {split_line[2]}\n"

        main_file.write(line)

#  replace all function names with function line numbers
print("replacing all function names with function line numbers") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if line.lower().startswith(("cal", "jmp", "jiz")):
            for key, value in jumps.items():
                line = line[:4] + line[4:].replace(key, str(value))
        main_file.write(line)

# capitalize all opcodes
print("capitalizing all opcodes") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        line = line.upper()
        main_file.write(line)

# change unsigned numbers to signed for ldi
print("changing unsigned numbers to signed for ldi") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if line.startswith("LDI"):
            if 256 > int(line.split()[2]) > 127:
                line = line.replace(line.split()[2], str(-(256 - int(line.split()[2]))))
        main_file.write(line)


# fill missing operands
print("filling missing operands") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if line.startswith(
            ("INC", "DEC", "RSH", "LSH", "INV", "LOD", "STR", "SPD")
        ):  # two operands
            if len(line.split()) == 2:  # one opcode, only one operand
                fragments = line.split()
                fragments.append(fragments[1])
                line = " ".join(fragments) + "\n"
        elif line.startswith(
            ("ADD", "SUB", "MLT", "DVS", "SQA", "SQR", "ORR", "AND", "XOR")
        ):  # three operands
            if len(line.split()) == 3:  # one opcode, only 2 operands
                fragments = line.split()
                fragments.append(fragments[1])
                line = " ".join(fragments) + "\n"
        main_file.write(line)


# remove last line
print("removing last line") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.read()
with open("Instructions Compiled", "w") as main_file:
    main_file.write(lines.rstrip("\n"))


# got rid because its built into the cpu now
# # print array
# print("printing array") if debug else None
# with open("Instructions Compiled", "r") as instruction_file:
#     lines = instruction_file.readlines()
# print("\n")
# instruction_array = [
#     tuple(
#         int(item) if re.match(r"^-?\d+$", item) else item
#         for item in line.strip().split()
#     )
#     for line in lines
# ]
# print(str(instruction_array) + "\n")


# # sample title
# print("sample titling") if debug else None
# with open("Instructions Compiled", "r") as instruction_file:
#     lines = instruction_file.readlines()
# with open("Instructions Compiled", "w") as main_file:
#     for line in lines:
#         main_file.write(line)
