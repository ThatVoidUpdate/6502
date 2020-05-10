"""
Program to generate a valid rom file to be executed by the 6502
It also imports the generated character set from the Charset.py program
"""

with open("rom.bin", "wb") as output:

    rom = []#Create the empty rom list

    for i in range(0x0, 0x8000):
        rom.append(bytes((0x00,))) #append 0x8000 zeros to the file, to make it the correct length

    characterRom = []
    with open("characterRom.bin", "rb") as charSet:
        characterRom = list(charSet.read()) #Import the rom binary, and add it to the character rom list

    characterRom = characterRom  + ([0x00] * (0x800 - len(characterRom))) #Pad the character rom to 0x800 in length, to fit in the allocated section of rom
    program = [0xa2, 0x00, 0xa0, 0x4e, 0x8a, 0x9d, 0x00, 0x02, 0x48, 0xe8, 0x88, 0xc0, 0x00, 0xd0, 0xf5, 0x00] #The program to be executed by the processor

    rom[0:len(characterRom)] = [bytes((x,)) for x in characterRom] #Convert the character rom to bytes
    rom[len(characterRom):len(characterRom) + len(program)] = [bytes((x,)) for x in program] #Convert the program to bytes

    rom[0x7ffc] = bytes((0x00,)) #Set the reset vector to the start of the code
    rom[0x7ffd] = bytes((0x88,)) # "

    output.write(b''.join(rom)) #Write the rom file
    print("Wrote file successfully")