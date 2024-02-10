with open("Instructions Uncompiled", "r") as instruction_file:
    with open("Instructions Compiled", "w") as compiled_file:
        function_names = []
        line_number = -1
        for line in instruction_file:
            if line.strip():  # skips and deletes empty lines
                line = line.split("#")[0].strip()  # removes comments
                if line.endswith(
                    ":"
                ):  # its the name of a function, logs the fnuction name and line number
                    function_name = line[:-1]
                    function_names.append({function_name: line_number})
                else:
                    compiled_file.write(line + "\n")
            line_number += 1
        print(function_names)
print("pass 1 complete")


with open("Instructions Compiled", "r") as compiled_file:
    lines = compiled_file.readlines()
for i, line in enumerate(lines):
    for function in function_names:
        for function_name, line_number in function.items():
            if function_name in line:
                lines[i] = line.replace(
                    function_name, str(line_number)
                )  # replaces function name with line number of function
with open("Instructions Compiled", "w") as compiled_file:
    compiled_file.writelines(lines)
print("pass 2 complete")


with open("Instructions Compiled", "r") as instruction_file:
    instructions_line = instruction_file.read().split("\n")
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
print("pass 3 complete")
