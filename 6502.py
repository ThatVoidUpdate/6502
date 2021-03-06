import instructions
import display

def FromHex(hexa: bytes) -> int:
    """
    Function to facilitate converting from hexadecimal to decimal.
    The 6502 processor is little-endian, so the data has to be converted from that format as well
    """
    return int.from_bytes(hexa, byteorder="little")


NMI_VECTOR = 0xfffa #Position of the non-maskable interrupt vector in memory
RESET_VECTOR = 0xfffc #Position of the reset vector in memory, which is where execution will start when the processor is powered on
IRQ_VECTOR = 0xfffe #Position of the IRQ vector in memory

#This is a dictionary holding the state of the machine, such as the memory, program counter and registers
machineState = {"MEMORY":[0x00]*0x10000,
                "PC":0x00,
                "X": 0x00,
                "Y": 0x00,
                "ACC": 0x00,
                "FLAGS": 0b00000000,
                "SP": 0xFF}


#Load the rom file
with open("rom.bin", "rb") as romFile:
    rom = romFile.read()


#Move the rom file into memory at location 0x0000
machineState["MEMORY"][0x0000:] = rom

#print(hex(len(rom)))

#Get the Reset vector, and set the program counter to that location, to begin execution from that memory address
machineState["PC"] = FromHex(machineState["MEMORY"][RESET_VECTOR:RESET_VECTOR+2])

print(f"Reset vector: {hex(machineState['PC'])}")

#Initialise a new screen
#screen = display.Display()

#Repeat forever
while True:
    #Get the instruction at the location of the program counter
    instruction = machineState["MEMORY"][machineState["PC"]]

    print(f"PC: {hex(machineState['PC'])}, ", end="")
    print(f"Current Opcode: {hex(instruction)}, ", end="") #Show opcode
    #print(f"Next memory: {' '.join([hex(x) for x in machineState['MEMORY'][machineState['PC']:machineState['PC']+16]])}") #Preview of next instructions


    #If the instruction is a valid instruction
    if instruction in instructions.switch_table:
        #Then call it, passing in the current state of the machine
        instructions.switch_table[instruction](machineState)
    else:
        instructions.Crash(machineState, "Invalid instruction (not in table)")

    #Update the screen
    #screen.UpdateScreen(machineState)