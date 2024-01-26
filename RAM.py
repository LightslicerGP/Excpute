def write(id: int, new_data: int, signed: bool = True):
    with open("RAM.bin", "rb") as file:
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

    with open("RAM.bin", "wb") as file:
        file.write(data)

def read(id: int, signed: bool = True):
    with open("RAM.bin", "rb") as f:
        value = f.read()[id]
    if not signed:  # 0 to 255
        return value
        # -128 to 127
    if value > 127:  # when sig bit is 1, meaning negative
        return -(256 - value)
    else:  # when sig bit is 0, meaning positive
        return value
