with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x8000):
        rom.append(bytes((0x00,)))

    program = [0xa0, 0x00, 0x98, 0x99, 0x00, 0x02, 0x48, 0xc8, 0xc0, 0xff, 0xd0, 0xf6]

    print(bytes(program))

    rom[0:len(program)] = [bytes((x,)) for x in program]

    rom[0x7ffc] = bytes((0x00,))
    rom[0x7ffd] = bytes((0x80,))

    print(len(rom))

    print(rom[:10])
    print(rom[-10:])

    output.write(b''.join(rom))
    print("Wrote file successfully")