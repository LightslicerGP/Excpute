import re

debug = False

with open("Instructions Uncompiled") as F:
    lines = [line.rstrip() for line in F]
print("\n", lines) if debug else None
print("-----------------------------------------") if debug else None


# remove comments
print("removing comments") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    lines[i] = line.split("#")[0].strip()
    i += 1

# remove extra lines
print("removing extra lines") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    if line == "":
        lines.pop(i)
        continue
    i += 1

# replace 0x and 0b with their decimal numbers
print("replacing 0x and 0b with their decimal numbers") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    if "0x" in line:
        pattern = r"0x[0-9a-fA-F]+"
        lines[i] = re.sub(pattern, lambda x: str(int(x.group(0), 16)), line)
    elif "0b" in line:
        pattern = r"0b[01]+"
        lines[i] = re.sub(pattern, lambda x: str(int(x.group(0), 2)), line)
    i += 1

# keep track of const names, and the value, then delete the lines
(
    print("keeping track of const names, and the value, then deleting the lines")
    if debug
    else None
)
constants = {}
i = 0
while i < len(lines):
    line = lines[i]
    if "=" in line:
        const_name, const_value = line.split("=")
        const_name = const_name.strip()
        const_value = int(const_value.strip())
        constants[const_name] = const_value
        lines.pop(i)
        continue
    i += 1
print("constants:", constants) if debug else None
constants = dict(sorted(constants.items(), key=lambda item: len(item[0]), reverse=True))
print("constants sorted:", constants) if debug else None

# keep track of function names, and the line number, then delete the lines
(
    print(
        "keeping track of function names, and the line number, then deleting the lines"
    )
    if debug
    else None
)
jumps = {}
i = 0
while i < len(lines):
    line = lines[i]
    if ":" in line:
        jump_name = line.split(":")[0]
        jumps[jump_name] = i
        lines.pop(i)
        continue
    i += 1
print("jumps:", jumps) if debug else None
jumps = dict(sorted(jumps.items(), key=lambda item: len(item[0]), reverse=True))
print("jumps sorted:", jumps) if debug else None


#  Replace all constants names with their values
print("replacing all constants names with their values") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    # for key, value in constants.items():
    #     line = line.replace(key, str(value))
    #     lines[i] = line
    if not line.lower().startswith(("cal", "jmp", "jiz")):
        for key, value in constants.items():
            line = line[:4] + line[4:].replace(key, str(value))
        lines[i] = line
    elif line.lower().startswith("jiz"):
        split_line = line.split()
        for key, value in constants.items():
            split_line[1] = split_line[1].replace(key, str(value))
        # print(lines[i])
        lines[i] = f"{split_line[0]} {split_line[1]} {split_line[2]}"
    i += 1


#  replace all function names with function line numbers
print("replacing all function names with function line numbers") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    if line.lower().startswith(("cal", "jmp", "jiz")):
        for key, value in jumps.items():
            line = line[:4] + line[4:].replace(key, str(value))
        lines[i] = line
    i += 1

# capitalize all opcodes
print("capitalizing all opcodes") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    lines[i] = line.upper()
    i += 1

# change unsigned numbers to signed for ldi
print("changing unsigned numbers to signed for ldi") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("LDI"):
        if 256 > int(line.split()[2]) > 127:
            line = line.replace(line.split()[2], str(-(256 - int(line.split()[2]))))
            lines[i] = line
    i += 1

# fill missing operands
print("filling missing operands") if debug else None
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith(
        ("INC", "DEC", "RSH", "LSH", "INV", "LOD", "STR", "SPD")
    ):  # two operands
        if len(line.split()) == 2:  # one opcode, only one operand
            fragments = line.split()
            fragments.append(fragments[1])
            line = " ".join(fragments)
    elif line.startswith(
        ("ADD", "SUB", "MLT", "DVS", "SQA", "SQR", "ORR", "AND", "XOR")
    ):  # three operands
        if len(line.split()) == 3:  # one opcode, only 2 operands
            fragments = line.split()
            fragments.append(fragments[1])
            line = " ".join(fragments)
    lines[i] = line
    i += 1

with open("Instructions Compiled", "w") as final_file:
    for i in range(len(lines)):
        if i == len(lines) - 1:
            final_file.write(lines[i])
        else:
            final_file.write(lines[i] + "\n")

# i = 0
# while i < len(lines):
#     line = lines[i]

#     i += 1

print(lines) if debug else None
