import re

debug = True

if debug:
    print(
        "Removing comments, removing empty lines, and assigning function names to line numbers and variables to values"
    )

with open("Instructions Uncompiled", "r") as instruction_file:
    with open("Instructions Compiled", "w") as compiled_file:
        named_items = {}
        line_number = 0
        for line in instruction_file:
            if line.strip():  # skips and deletes empty lines

                line = line.split("#")[0].strip()  # removes comments

                if ("0x" or "0b") in line:
                    line = line.split(" ")
                    for item in line:
                        if item_value.startswith("0b"):
                            item = int(item, 16)
                        elif item.startswith("0b"):
                            item = int(item, 2)

                if line.endswith(":"):  # its the name of a function
                    item_name = line[:-1]
                    named_items[item_name] = line_number

                elif "=" in line:  # constant is being assigned
                    parts = line.split("=")
                    item_name = parts[0].strip()
                    item_value = parts[1].strip()
                    named_items[item_name] = item_value

                else:
                    words = line.split()
                    words[0] = words[0].lower()  # Convert first word to lowercase
                    line = " ".join(words)
                    compiled_file.write(line + "\n")
                    line_number += 1
        if debug:
            print("variables/functions and their values:")
            print(named_items)

# print("test") if debug else None
if debug:
    print("pass 1 complete")
    print("Replaceing function names with line numbers")

with open("Instructions Compiled", "r") as compiled_file:
    lines = compiled_file.readlines()

for variable_name, variable_value in named_items.items():
    for i, line in enumerate(lines):
        lines[i] = line.replace(variable_name, str(variable_value))

with open("Instructions Compiled", "w") as compiled_file:
    compiled_file.writelines(lines)


if debug:
    print("pass 2 complete")
    print("combining addition parts")


with open("Instructions Compiled", "r") as compiled_file:
    lines = compiled_file.readlines()
with open("Instructions Compiled", "w") as compiled_file:
    for line in lines:
        line = line.strip("\n")
        pattern = r"(\d+)\+(\d+)"

        def replace_expression(match):
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            return str(result)

        modified_line = re.sub(pattern, replace_expression, line)
        compiled_file.write(modified_line + "\n")

if debug:
    print("pass 3 complete")
    print("converting instructions into array form")

with open("Instructions Compiled", "r") as instruction_file:
    instructions_line = instruction_file.read().replace(",", "").split("\n")
    instructions = []

    for instruction_set in instructions_line:
        instruction_tuple = instruction_set.split(" ")
        instruction_data = [
            (
                int(item)
                if item.isdigit() or (item[0] == "-" and item[1:].isdigit())
                else item
            )
            for item in instruction_tuple[1:]
        ]

        if len(instruction_data) == 4 and instruction_data[3] == 0:
            instructions.append((instruction_tuple[0], *instruction_data, 0))
        else:
            instructions.append((instruction_tuple[0], *instruction_data))

    print(instructions[:-1])

if debug:
    print("pass 4 complete")
