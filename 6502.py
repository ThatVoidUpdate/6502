import instructions

def FromHex(hexa: bytes) -> int:
    return int.from_bytes(hexa, byteorder="little")

NMI_VECTOR = 0xfffa
RESET_VECTOR = 0xfffc
IRQ_VECTOR = 0xfffe

machineState = {"ROM":[], 
                "RAM":[0x0]*0x10000, 
                "PC":0x00,
                "X": 0x00,
                "Y": 0x00,
                "ACC": 0x00,
                "FLAGS": 0b00000000,
                "SP": 0xFF}


with open("rom.bin", "rb") as romFile:
    machineState["ROM"] = romFile.read()

#print(hex(len(machineState["rom"])))

#verify rom is correct
if len(machineState["ROM"]) != 0x10000:
    print("Rom has an invalid length")
    exit()

machineState["PC"] = FromHex(machineState["ROM"][RESET_VECTOR:RESET_VECTOR+2])

print(f"Reset vector: {machineState['PC']}")

while True:
    instruction = machineState["ROM"][machineState["PC"]]
    #print(hex(instruction))

    if instruction in instructions.switch_table:
        instructions.switch_table[instruction](machineState)
        input()