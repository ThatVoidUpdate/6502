with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x10000):
        
        rom.append(bytes((0xea,)))

    rom[0x0] = bytes((0xa9,))
    rom[0x1] = bytes((0x80,))

    rom[0x2] = bytes((0x85,))
    rom[0x3] = bytes((0x01,))

    rom[0x4] = bytes((0x65,))
    rom[0x5] = bytes((0x01,))

    rom[0x6] = bytes((0x00,))

    rom[0xfffc] = bytes((0x00,))
    rom[0xfffd] = bytes((0x00,))

    print(rom[:10])

    output.write(b''.join(rom))