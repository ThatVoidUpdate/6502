with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x8000):
        rom.append(bytes((0x00,)))

    program = [0xa9, 0x03, 0x4c, 0x08, 0x80, 0x00, 0x00, 0x00, 0x8d, 0x00, 0x02]

    rom[0:len(program)] = [bytes((x,)) for x in program]

    rom[0x7ffc] = bytes((0x00,))
    rom[0x7ffd] = bytes((0x80,))

    output.write(b''.join(rom))
    print("Wrote file successfully")