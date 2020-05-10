import instructions
import display

def FromHex(hexa: bytes) -> int:
    return int.from_bytes(hexa, byteorder="little")

NMI_VECTOR = 0xfffa
RESET_VECTOR = 0xfffc
IRQ_VECTOR = 0xfffe

machineState = {"MEMORY":[0x0]*0x10000,
                "PC":0x00,
                "X": 0x00,
                "Y": 0x00,
                "ACC": 0x00,
                "FLAGS": 0b00000000,
                "SP": 0xFF}


with open("rom.bin", "rb") as romFile:
    rom = romFile.read()

#verify rom is correct
if len(rom) != 0x8000:
    print("Rom has an invalid length")
    exit()

machineState["MEMORY"][0x8000:] = rom

print(hex(len(rom)))

machineState["PC"] = FromHex(machineState["MEMORY"][RESET_VECTOR:RESET_VECTOR+2])

print(f"Reset vector: {hex(machineState['PC'])}")

print(machineState["MEMORY"][0x8000:0x8005])

screen = display.Display()

while True:
    instruction = machineState["MEMORY"][machineState["PC"]]

    #print(hex(instruction))

    if instruction in instructions.switch_table:
        instructions.switch_table[instruction](machineState)

    screen.UpdateScreen(machineState)