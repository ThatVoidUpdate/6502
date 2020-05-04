with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x10000):
        
        rom.append(bytes((0xea,)))

    program = [0xa9, 0x01, 0x0a, 0x10, 0xfd, 0x00]
    
    print(bytes(program))

    rom[0:len(program)] = [bytes((x,)) for x in program]

    rom[0xfffc] = bytes((0x00,))
    rom[0xfffd] = bytes((0x00,))

    print(rom[:10])

    output.write(b''.join(rom))
    print("Wrote file successfully")