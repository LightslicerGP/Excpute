const { ram_read, ram_write } = require("./RAM");
const { init_display, update_display } = require("./Display");
const fs = require("fs");

var registers = Array(8).fill(0);

const debug = false;
const print_registers = false;

function reg_read(id, signed = true) {
  let value = registers[id];
  if (!signed) {
    // 0 to 255
    return value;
  }
  // -128 to 127
  if (value > 127) {
    // when sig bit is 1, meaning negative
    return -(256 - value);
  } else {
    // when sig bit is 0, meaning positive
    return value;
  }
}

function reg_write(id, new_data, signed = true) {
  //   console.log(id, new_data);
  if (signed && -128 <= new_data < 0) {
    // converts the negative number to unsigned number
    registers[id] = 256 + new_data;
  } else if ((!signed && 0 <= new_data <= 255) || (signed && 0 <= new_data <= 127)) {
    // sb doesnt matter, write number
    registers[id] = new_data;
  } else {
    throw new Error(`Cannot write ${new_data} to register ${id}`);
  }
}

function flag_read(flag) {
  switch (flag) {
    case "carry":
      return reg_read(6, false) & 0b00000001;
    case "zero":
      return reg_read(6, false) & 0b00000010;
    case "parity":
      return reg_read(6, false) & 0b00000100;
    case "negative":
      return reg_read(6, false) & 0b00001000;
    case "overflow":
      return reg_read(6, false) & 0b00010000;
    default:
      throw new Error(`Flag must be carry, zero, parity, overflow, or negative`);
  }
}

function flag_set(flag, sign) {
  if (sign == 0) {
    switch (flag) {
      case "carry":
        reg_write(6, reg_read(6, false) & 0b11111110, false);
        break;
      case "zero":
        reg_write(6, reg_read(6, false) & 0b11111101, false);
        break;
      case "parity":
        reg_write(6, reg_read(6, false) & 0b11111011, false);
        break;
      case "negative":
        reg_write(6, reg_read(6, false) & 0b11110111, false);
        break;
      case "overflow":
        reg_write(6, reg_read(6, false) & 0b11101111, false);
        break;
      default:
        throw new Error(`Flag must be carry, zero, parity, overflow, or negative`);
    }
  } else if (sign == 1) {
    switch (flag) {
      case "carry":
        reg_write(6, reg_read(6, false) | 0b00000001, false);
        break;
      case "zero":
        reg_write(6, reg_read(6, false) | 0b00000010, false);
        break;
      case "parity":
        reg_write(6, reg_read(6, false) | 0b00000100, false);
        break;
      case "negative":
        reg_write(6, reg_read(6, false) | 0b00001000, false);
        break;
      case "overflow":
        reg_write(6, reg_read(6, false) | 0b00010000, false);
        break;
      default:
        throw new Error(`Flag must be carry, zero, parity, overflow, or negative`);
    }
  } else {
    throw new Error("Flag write number must be 1 or 0");
  }
}

instruction_address = reg_read(7, false);

function next_instruction() {
  if (instruction_address == 255) {
    reg_write(7, 0, false);
  } else {
    reg_write(7, instruction_address + 1, false);
  }
}

function execute(opcode, operands) {
  switch (opcode) {
    case "NOP":
      next_instruction();
      break;
    case "HLT":
      // process.exit()
      console.log("Exiting program execution...");
      // what do i do here?
      break;
    case "ADD":
      var regA = operands[0];
      var regB = operands[1];
      var regDest = operands[2];
      var SetFlag = operands.length > 3 ? operands[3] : 1;
      var CarryFlag = operands.length > 4 ? operands[4] : 0;

      var A = reg_read(regA, false);
      var B = reg_read(regB, false);

      if (CarryFlag === 1) {
        result = A + B + flag_read(carry);
      } else {
        result = A + B;
      }

      if (result > 255) {
        if (SetFlag === 1) {
          flag_set("carry", 1);
        }
        result -= 256;
      }

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "SUB":
      var regA = operands[0];
      var regB = operands[1];
      var regDest = operands[2];
      var SetFlag = operands.length > 3 ? operands[3] : 1;

      var A = reg_read(regA, true);
      var B = reg_read(regB, true);

      var result = A - B;

      if (result > 127) {
        result -= 256;
      } else if (result < -128) {
        if (SetFlag === 1) {
          flag_set("carry", 1);
        }
        result += 256;
      }

      reg_write(regDest, result);
      next_instruction();
      break;
    case "ORR":
      var regA = operands[0];
      var regB = operands[1];
      var regDest = operands[2];

      var A = reg_read(regA, false);
      var B = reg_read(regB, false);

      var result = A | B;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "AND":
      var regA = operands[0];
      var regB = operands[1];
      var regDest = operands[2];

      var A = reg_read(regA, false);
      var B = reg_read(regB, false);

      var result = A & B;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "XOR":
      var regA = operands[0];
      var regB = operands[1];
      var regDest = operands[2];

      var A = reg_read(regA, false);
      var B = reg_read(regB, false);

      var result = A ^ B;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "INV":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA, false);

      var result = A ^ 255;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "INC":
      var regA = operands[0];
      var regDest = operands[1];
      var SetFlag = operands.length > 2 ? operands[2] : 1;

      var A = reg_read(regA, false);
      var result;

      if (A === 255) {
        if (SetFlag === 1) {
          flag_set("carry", 1);
        }
        result = 0;
      } else {
        result = A + 1;
      }

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "DEC":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA, false);
      var result;

      if (A === 0) {
        result = 255;
      } else {
        result = A - 1;
      }

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "RSH":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA, false);

      var result = A >> 1;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "LSH":
      var regA = operands[0];
      var regDest = operands[1];
      var SetFlag = operands.length > 2 ? operands[2] : 1;

      var A = reg_read(regA, false);

      var result = A << 1;

      if (result > 255) {
        if (SetFlag === 1) {
          flag_set("carry", 1);
        }
        result -= 256;
      }

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "RBS":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA, false);

      var result = (A >> 1) | ((A << 7) & 255);

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "LBS":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA, false);

      var result = ((A << 1) | (A >> 7)) & 255;

      reg_write(regDest, result, false);
      next_instruction();
      break;
    case "CMP":
      var regA = operands[0];
      var regB = operands[1];

      var A = reg_read(regA);
      var B = reg_read(regB);

      var result = B - A;

      if (result === 0) {
        flag_set("zero", 1);
      } else {
        flag_set("zero", 0);
      }

      if (result > 0) {
        flag_set("negative", 1);
      } else {
        flag_set("negative", 0);
      }

      if (result < 0) {
        flag_set("carry", 1);
      } else {
        flag_set("carry", 0);
      }

      next_instruction();
      break;
    case "PSH":
      var regA = operands[0];

      var A = reg_read(regA, false);
      var stack_pointer = reg_read(5, false);

      ram_write(stack_pointer, A, false); // writes to stack
      reg_write(5, stack_pointer - 1, false); // "increments" (decrements) pointer
      next_instruction();
      break;
    case "POP":
      var regDest = operands[0];

      var stack_pointer = reg_read(5, false);

      var pointer_data = ram_read(stack_pointer + 1, false); // reads last pointer location
      reg_write(regDest, pointer_data, false); // writes from stack
      reg_write(5, stack_pointer + 1, false); // "decrements" (increments) pointer

      next_instruction();
      break;
    case "CAL":
      var jump_to = operands[0];

      var stack_pointer = reg_read(5, false);

      ram_write(stack_pointer, instruction_address + 1, false); // writes to stack
      reg_write(5, stack_pointer - 1, false); // "increments" (decrements) pointer
      reg_write(7, jump_to, false); // jumps to new instruction address
      // instead of running next_instruction()
      break;
    case "RTN":
      var stack_pointer = reg_read(5, false);
      var pointer_data = ram_read(stack_pointer + 1, false); // reads last pointer location
      reg_write(5, stack_pointer + 1, false); // "decrements" (increments) pointer
      reg_write(7, pointer_data, false); // returns to the instruction address
      break;
    case "CPY":
      var regA = operands[0];
      var regDest = operands[1];

      var data = reg_read(regA);

      reg_write(regDest, data);
      next_instruction();
      break;
    case "LDI":
      var address = operands[0];
      var number = operands[1];

      reg_write(address, number);
      next_instruction();
      break;
    case "LOD":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA);
      var data = ram_read(A);

      reg_write(regDest, data);
      next_instruction();
      break;
    case "STR":
      var regA = operands[0];
      var regDest = operands[1];

      var A = reg_read(regA);
      var Destination = reg_read(regDest, false);

      ram_write(Destination, A);
      next_instruction();
      break;
    case "PTI":
      var address = operands[0];
      var regDest = operands[1];

      var data = port_read(address);

      reg_write(regDest, data);
      next_instruction();
      break;
    case "PTO":
      var regA = operands[0];
      var address = operands[1];

      port_write(regA, address);
      next_instruction();
      break;
    case "JMP":
      var address = operands[0];

      reg_write(7, address, false);
      break;
    case "JIZ":
      var regA = operands[0];
      var address = operands[1];

      var A = reg_read(regA);

      if (A === 0) {
        reg_write(7, address, false);
      } else {
        next_instruction();
      }
      break;
    case "SPD":
      var regA = operands[0];
      var property = operands[1];
      var mode = operands.length > 2 ? operands[2] : 0;

      var A = reg_read(regA, false);

      if (mode === 0) {
        if (property < 5) {
          // r, g, b, x, y
          var ram_address = property + 250; // 0 -> 250, 4 -> 254
          ram_write(ram_address, A, false);
        } else if (property >= 5) {
          // set, fill, update
          var ram_data = property - 4; // 5 -> 1, 7 -> 3
          ram_write(255, ram_data, false);
          update_display(); // update this
        }
      } else if (mode === 1) {
        x_coordinate = ram_read(253, false) * scale;
        y_coordinate = (255 - ram_read(254, false)) * scale;

        if (property == 0) {
          reg_write(regA);
        }
        if (property == 1) {
          reg_write(regA);
        }
        if (property == 2) {
          reg_write(regA);
        }
        if (property == 3 || property == 4) {
          ram_address = property + 250; // 3 -> 253, 4 -> 254
        } else if (property >= 5) {
          console.log("mode is set/fill/push, and reading from screen?");
        }
      }

      next_instruction();
      break;
    default:
      throw new Error("Invalid opcode");
  }
}

function get_instructions(file_name) {
  const fileContent = fs.readFileSync(file_name, "utf8");
  const instruction_array = [];

  const lines = fileContent.split("\r\n");

  lines.forEach((line) => {
    var [opcode, ...operands] = line.split(" ");
    if (operands.length == 0) {
      instruction_array.push([opcode]);
    } else {
      var operands = operands.map((operand) => parseInt(operand, 10)); // base 10
      instruction_array.push([opcode, operands]);
    }
  });
  //   const instruction_array_json = JSON.stringify(instruction_array);
  //   fs.writeFileSync("instruction_array.json", instruction_array_json);
  return instruction_array;
}

function update_cpu(program) {
  if (instruction_address < 256) {
    const opcode = program[instruction_address][0];
    const operands = program[instruction_address][1];
    execute(opcode, operands);

    instruction_address = reg_read(7, false);
  } else {
    console.log("Ran out of instructions, halted automatically");

    process.exit(0);
  }
}
const scale = 4;

init_display(scale);

const program = get_instructions("Instructions Compiled");
reg_write(7, 0, false); // set instruction address
reg_write(5, 249, false); // set stack address

const running = true;

while (running) {
  update_cpu();
}

// console.log(get_instructions("Instructions Compiled"));

// execute("LDI", [1, 0b00110101]);
// console.log(registers);
// execute("CMP", [1, 2]);
// console.log(registers);

// registers.forEach((register, index) => {
//   console.log(`Register ${index}: ${register.toString(2)}, ${register}`);
// });
