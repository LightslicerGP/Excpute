reg_a_data = '11111111'
reg_b_data = '00000011'
flag_state = 0

squared_number_dec = int(reg_a_data, 2) ** int(reg_b_data, 2)
squared_number_bin = '00000000'
flag = 0

if squared_number_dec > 255:
    squared_number_bin = '00000000'
    if flag_state == 1:
        flag = 1

else:
    squared_number_bin = bin(squared_number_dec)[
        2:].zfill(8)  # trim to right 3


print(squared_number_dec, squared_number_bin, flag)

"""
whole_number, whole_remainder = divmod(int(reg_a_data, 2), int(reg_b_data, 2))
whole_number_binary = bin(whole_number)[2:].zfill(8)

remainder = float(whole_remainder) / float(int(reg_b_data, 2))
remainder_binary = ""
for _ in range(8):
    remainder *= 2
    binary_digit = int(remainder)
    remainder_binary += str(binary_digit)
    remainder -= binary_digit

whole_remainder_binary = bin(whole_number)[2:].zfill(8)

print("Whole Number (Binary): " + whole_number_binary)
print("Non-Decimal Result (Binary): " + whole_remainder_binary)
print("Remainder Result (Binary): " + remainder_binary)



def next_register(reg_id):
    if reg_id == '111':
        return '000'
    else:
        dec_id = int(reg_id, 2)
        dec_id += 1
        return bin(dec_id)[2:].zfill(3)

register_example = '111'
print("current register: ", register_example,
      ", next register", next_register(register_example))





def fraction_to_binary(numerator, denominator):

    if denominator == 0:
        raise ValueError("Denominator cannot be zero.")

    # Get the greatest common divisor of the numerator and denominator.
    gcd = math.gcd(numerator, denominator)

    # Divide the numerator and denominator by the greatest common divisor.
    numerator //= gcd
    denominator //= gcd

    # Convert the numerator and denominator to binary.
    binary_numerator = bin(numerator)[2:]
    binary_denominator = bin(denominator)[2:]

    # Pad the binary representation of the numerator with zeros to the same length as the binary representation of the denominator.
    binary_numerator = binary_numerator.zfill(8)

    # Return the binary representation of the fraction.
    return binary_numerator + binary_denominator


print(fraction_to_binary(whole_remainder, int(reg_b_data, 2)))

print(divmod(int(reg_a, 2), int(reg_b, 2)))





flag = '0'

if len(result) <= 8:
    print(result.zfill(8))
else:
    flag = '1'
    result = result[1:]
    print(result, flag)

string = 'abcdefghijklmnopqrstuvwxyz'
print(string[:5])
print(string[5:13])


def bin2num(bin):
    return int(bin, 2)


def num2bin(num):
    return bin(int(num))


print(bin2num('111111111111'))

print(num2bin('127'))
"""
