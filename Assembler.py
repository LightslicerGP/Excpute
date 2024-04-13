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
        main_file.write(line)
        line_number += 1
    print("jumps:", jumps) if debug else None

#  Replace all constants names with their values
print("replacing all constants names with their values") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        for key, value in constants.items():
            line = line.replace(key, str(value))
        main_file.write(line)

#  replace all function names with function line numbers
print("replacing all function names with function line numbers") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        if line.lower().startswith(("cal", "jmp", "jiz")):
            for key, value in jumps.items():
                line = line.replace(key, str(value))
        main_file.write(line)

# capitalize all opcodes
print("capitalizing all opcodes") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
with open("Instructions Compiled", "w") as main_file:
    for line in lines:
        line = line.upper()
        main_file.write(line)


# remove last line
print("removing last line") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.read()
with open("Instructions Compiled", "w") as main_file:
    main_file.write(lines.rstrip("\n"))


# print array
print("printing array") if debug else None
with open("Instructions Compiled", "r") as instruction_file:
    lines = instruction_file.readlines()
print("\n")
instruction_array = [
    tuple(
        int(item) if re.match(r"^-?\d+$", item) else item
        for item in line.strip().split()
    )
    for line in lines
]
print(str(instruction_array) + "\n")


# # sample title
# print("sample titling") if debug else None
# with open("Instructions Compiled", "r") as instruction_file:
#     lines = instruction_file.readlines()
# with open("Instructions Compiled", "w") as main_file:
#     for line in lines:
#         main_file.write(line)
