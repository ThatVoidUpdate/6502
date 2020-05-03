def FromHex(hexa: bytes) -> int:
    return int.from_bytes(hexa, byteorder="little")

NMI_VECTOR = 0xfffa
RESET_VECTOR = 0xfffc
IRQ_VECTOR = 0xfffe

rom = []

with open("rom.bin", "rb") as romFile:
    rom = romFile.read()

print(hex(len(rom)))

#verify rom is correct
if len(rom) != 0x10000:
    print("Rom has an invalid length")
    exit()

ProgramCounter = FromHex(rom[RESET_VECTOR:RESET_VECTOR+2])

print(f"Reset vector: {ProgramCounter}")

instruction = hex(rom[ProgramCounter])
print(instruction)

