with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x8000):
        
        rom.append(bytes((0xea,)))

    program = [0xa9, 0x01, 0x0a, 0x10, 0xfe, 0x00]
    
    print(bytes(program))

    rom[0:len(program)] = [bytes((x,)) for x in program]

    rom[0x7ffc] = bytes((0x00,))
    rom[0x7ffd] = bytes((0x80,))

    print(len(rom))

    print(rom[:10])
    print(rom[-10:])

    output.write(b''.join(rom))
    print("Wrote file successfully")