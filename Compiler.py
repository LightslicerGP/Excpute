# im going to convert the "instruction" file
# into the "assembled instruction example",
# probably WITH call and return (because i
# dont want to edit the iso AGAIN lmao)
# i dont know how to do that yet, but it
# isnt really priority, first the CPU then this
def reset():
    with open("Registers.bin", "wb") as f:
        print("writing register file")
        f.write(bytearray([0] * 8))
    with open("RAM.bin", "wb") as f:
        print("writing RAM file")
        f.write(bytearray([0] * 256))
