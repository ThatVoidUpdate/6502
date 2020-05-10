with open("rom.bin", "wb") as output:

    rom = []

    for i in range(0x0, 0x8000):
        rom.append(bytes((0x00,)))

    characterRom = []
    with open("characterRom.bin", "rb") as charSet:
        characterRom = list(charSet.read())

    characterRom = characterRom  + ([0x00] * (0x800 - len(characterRom)))
    program = [0xa2, 0x00, 0xa0, 0x4e, 0x8a, 0x9d, 0x00, 0x02, 0x48, 0xe8, 0x88, 0xc0, 0x00, 0xd0, 0xf5, 0x00]

    rom[0:len(characterRom)] = [bytes((x,)) for x in characterRom]
    rom[len(characterRom):len(characterRom) + len(program)] = [bytes((x,)) for x in program]

    rom[0x7ffc] = bytes((0x00,))
    rom[0x7ffd] = bytes((0x88,))

    output.write(b''.join(rom))
    print("Wrote file successfully")