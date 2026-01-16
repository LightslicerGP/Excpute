RAM = [0] * 256


def read(id: int, signed: bool = True):
    value = RAM[id]
    if not signed:  # 0 to 255
        return value
        # -128 to 127
    if value > 127:  # when sig bit is 1, meaning negative
        return -(256 - value)
    else:  # when sig bit is 0, meaning positive
        return value


def write(id: int, new_data: int, signed: bool = True):
    if (
        signed and -128 <= new_data < 0
    ):  # converts the negative number to unsigned number
        RAM[id] = 256 + new_data
    elif (not signed and 0 <= new_data <= 255) or (
        signed and 0 <= new_data <= 127
    ):  # sb doesnt matter, write number
        RAM[id] = new_data
    else:
        raise OverflowError(f"Cannot write {new_data} to ram register {id}")
