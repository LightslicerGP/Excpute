var RAM = Array(256).fill(0);

function ram_read(id, signed_value = true) {
  let value = RAM[id];
  if (!signed_value) {
    return value;
  }
  if (value > 127) {
    return -(256 - value);
  } else {
    return value;
  }
}

function ram_write(id, new_data, signed_value = true) {
  if (signed_value && -128 <= new_data && new_data < 0) {
    RAM[id] = 256 + new_data;
  } else if ((!signed_value && 0 <= new_data && new_data <= 255) || (signed_value && 0 <= new_data && new_data <= 127)) {
    RAM[id] = new_data;
  } else {
    throw new Error(`Cannot write ${new_data} to register ${id}`);
  }
}

module.exports = { ram_read, ram_write };
