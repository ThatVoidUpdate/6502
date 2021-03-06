"""
This file contains all the code for the individual instructions of the 6502 processor.
The functions are named for their corresponding hex opcode, to make calling them easier to keep track of
"""

import config


def Crash(machineState: dict, Reason: str):
    print(f"Crash while executing at {hex(machineState['PC'])}: \"{Reason}\"")
    print(f"Opcode: {hex(machineState['MEMORY'][machineState['PC']])}")
    print(f"ACC: {hex(machineState['ACC'])}, X: {hex(machineState['X'])}, Y: {hex(machineState['Y'])}, Flags: {bin(machineState['FLAGS'])}")
    exit()

def FromHex(hexa: bytes) -> int:
    """
    Function to facilitate converting from hexadecimal to decimal.
    The 6502 processor is little-endian, so the data has to be converted from that format as well
    """
    return int.from_bytes(hexa, byteorder="little")


def opcode_00(machineState: dict):
    #BRK Implied 1 7
    if config.VERBOSE:
        print("BRK hit, exiting")
        print(f"ACC: {hex(machineState['ACC'])}, X: {hex(machineState['X'])}, Y: {hex(machineState['Y'])}, Flags: {bin(machineState['FLAGS'])}")
    if config.INPUT_ON_BRK:
        input()
    exit()

def opcode_01(machineState: dict):
    #ORA (IND, X) 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte]))
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2


def opcode_05(machineState: dict):
    #ORA ZP 2 6
    data = machineState["MEMORY"][machineState["MEMORY"][machineState["PC"] + 1]]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_06(machineState: dict):
    #ASL ZP 2 5
    address = machineState["MEMORY"][machineState["PC"] + 1]

    machineState["MEMORY"][address] *= 2

    if machineState["MEMORY"][address] > 0xff: #carry flag
        machineState["MEMORY"][address] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["MEMORY"][address] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Shifted {hex(address)} left once (now {machineState['MEMORY'][address]})")

    machineState["PC"] += 2

def opcode_08(machineState: dict):
    #PHP Implied 1 3

    address = 0x0100 + machineState["SP"]
    machineState["MEMORY"][address] = machineState["FLAGS"]
    machineState["SP"] -= 1

    if config.VERBOSE:
        print(f"Pushed processor flags ({bin(machineState['FLAGS'])} to stack)")

    machineState["PC"] += 1

def opcode_09(machineState: dict):
    #ORA IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]
    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_0a(machineState: dict):
    #ASL accum 1 2
    machineState["ACC"] *= 2

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Shifted acc left once (now {machineState['ACC']})")

    machineState["PC"] += 1

def opcode_0d(machineState: dict):
    #ORA ABS 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3

def opcode_0e(machineState: dict):
    #ASL ABS 3 6
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])

    machineState["MEMORY"][address] *= 2

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Shifted {hex(address)} left once (now {machineState['ACC']})")

    machineState["PC"] += 3



def opcode_10(machineState: dict):
    #BPL Relative 2 2
    #if negative flag clear, add offset to PC and resume execution
    if machineState["FLAGS"] & 0b10000000 == 0b00000000:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 1
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because negative flag was clear")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because negative flag was not clear")

def opcode_11(machineState: dict):
    #ORA (IND), Y 2 5

    address = machineState["MEMORY"][machineState["PC"] + 1]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte])) + machineState["Y"]
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_15(machineState: dict):
    #ORA ZP,X 2 5

    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_16(machineState: dict):
    #ASL ZP,X 2 6

    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]

    machineState["MEMORY"][address] *= 2

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Shifted {hex(address)} left once (now {machineState['MEMORY'][address]})")

    machineState["PC"] += 2

def opcode_18(machineState: dict):
    #CLC Implied 1 2
    machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if config.VERBOSE:
        print("Cleared carry bit of processor flags")

    machineState["PC"] += 1

def opcode_19(machineState: dict):
    #ORA ABS,Y 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["Y"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3

def opcode_1d(machineState: dict):
    #ORA ABS,X 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] | data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3

def opcode_1e(machineState: dict):
    #ASL ABS,X 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]

    machineState["MEMORY"][address] *= 2

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Shifted {hex(address)} left once (now {machineState['MEMORY'][address]})")

    machineState["PC"] += 3


def opcode_20(machineState: dict):
    #JSR ABS 3 6
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])

    machineState["PC"] += 3

    machineState["MEMORY"][0x0100 + machineState["SP"]] = machineState["PC"] >> 8
    machineState["SP"] -= 1
    machineState["MEMORY"][0x0100 + machineState["SP"]] = machineState["PC"] & 0xFF
    machineState["SP"] -= 1

    machineState["PC"] = address

    if config.VERBOSE:
        print(f"Jumped to subroutine {hex(address)}")


def opcode_21(machineState: dict):
    #AND (IND, X) 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte]))
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_24(machineState: dict):
    #BIT ZP 2 3
    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]
    res = machineState["ACC"] & data

    if res == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if res & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if res & 0b01000000 == 0b01000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b01000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b10111111

    if config.VERBOSE:
        print(f"Bit test on {hex(address)}")

    machineState["PC"] += 2


def opcode_25(machineState: dict):
    #AND ZP 2 3
    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(address)}")

    machineState["PC"] += 2


def opcode_26(machineState: dict):
    #ROL ZP 2 5
    address = machineState["MEMORY"][machineState["PC"] + 1]

    machineState["MEMORY"][address] = machineState["MEMORY"][address] << 1
    machineState["MEMORY"][address] = machineState["MEMORY"][address] | (machineState["FLAGS"] & 0b00000001)
    if machineState["MEMORY"][address] & 0b100000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
        machineState["MEMORY"][address] -= 0b100000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Rotated {hex(address)} by one step left")

    machineState["PC"] += 2

def opcode_28(machineState: dict):
    #PLP Implied 1 3
    #stack operation: write to 0x0100 + SP, dec SP
    machineState["SP"] += 1
    address = 0x0100 + machineState["SP"]
    machineState["FLAGS"] = machineState["MEMORY"][address]

    if config.VERBOSE:
        print(f"Pulled processor flags ({bin(machineState['FLAGS'])} from stack)")

    machineState["PC"] += 1

def opcode_29(machineState: dict):
    #AND IMMIDIATE 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(data)}")

    machineState["PC"] += 2

def opcode_2a(machineState: dict):
    #ROL ACCUM 1 2

    machineState["ACC"] = machineState["ACC"] << 1
    machineState["ACC"] = machineState["ACC"] | (machineState["FLAGS"] & 0b00000001)
    if machineState["ACC"] & 0b100000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
        machineState["ACC"] -= 0b100000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Rotated ACC by one step left")

    machineState["PC"] += 1

def opcode_2c(machineState: dict):
    #BIT ABS 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]
    res = machineState["ACC"] & data

    if res == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if res & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if res & 0b01000000 == 0b01000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b01000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b10111111

    if config.VERBOSE:
        print(f"Bit test on {hex(address)}")

    machineState["PC"] += 3


def opcode_2d(machineState: dict):
    #AND ABS 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(address)}")

    machineState["PC"] += 3

def opcode_2e(machineState: dict):
    #ROL ABS 3 6
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])

    machineState["MEMORY"][address] = machineState["MEMORY"][address] << 1
    machineState["MEMORY"][address] = machineState["MEMORY"][address] | (machineState["FLAGS"] & 0b00000001)
    if machineState["MEMORY"][address] & 0b100000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
        machineState["MEMORY"][address] -= 0b100000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Rotated {hex(address)} by one step left")

    machineState["PC"] += 3


def opcode_30(machineState: dict):
    #BMI Relative 2 2
    #if negative flag set, add offset to PC and resume execution
    if machineState["FLAGS"] & 0b10000000 == 0b10000000:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 1
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because negative flag was set")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because negative flag was not set")

def opcode_31(machineState: dict):
    #AND (IND),Y 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte])) + machineState["Y"]
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_35(machineState: dict):
    #AND ZP,X 2 3
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(address)}")

    machineState["PC"] += 2

def opcode_36(machineState: dict):
    #ROL ZP,X 2 5
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]

    machineState["MEMORY"][address] = machineState["MEMORY"][address] << 1
    machineState["MEMORY"][address] = machineState["MEMORY"][address] | (machineState["FLAGS"] & 0b00000001)
    if machineState["MEMORY"][address] & 0b100000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
        machineState["MEMORY"][address] -= 0b100000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Rotated {hex(address)} by one step left")

    machineState["PC"] += 2

def opcode_38(machineState: dict):
    #SEC Implied 1 2
    machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001

    if config.VERBOSE:
        print("Set carry bit of processor flags")

    machineState["PC"] += 1

def opcode_39(machineState: dict):
    #AND ABS,Y 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["Y"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(data)}")

    machineState["PC"] += 3

def opcode_3d(machineState: dict):
    #AND ABS,X 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] & data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical and between ACC and {hex(data)}")

    machineState["PC"] += 3

def opcode_3e(machineState: dict):
    #ROL ABS,X 3 6
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]

    machineState["MEMORY"][address] = machineState["MEMORY"][address] << 1
    machineState["MEMORY"][address] = machineState["MEMORY"][address] | (machineState["FLAGS"] & 0b00000001)
    if machineState["MEMORY"][address] & 0b100000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
        machineState["MEMORY"][address] -= 0b100000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Rotated {hex(address)} by one step left")

    machineState["PC"] += 3


def opcode_40(machineState: dict):
    #RTI Implied 1 6
    machineState["SP"] += 1
    address = 0x0100 + machineState["SP"]
    machineState["FLAGS"] = machineState["MEMORY"][address]
    machineState["SP"] += 1
    address = 0x0100 + machineState["SP"]
    machineState["PC"] = machineState["MEMORY"][address]

    if config.VERBOSE:
        print(f"Pulled processor flags ({bin(machineState['FLAGS'])} and PC from stack)")

    machineState["PC"] += 1


def opcode_41(machineState: dict):
    #EOR (IND,X) 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte]))
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2


def opcode_45(machineState: dict):
    #EOR ZP 2 3
    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_46(machineState: dict):
    #LSR ZP 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1]

    if machineState["MEMORY"][address] & 0b1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    machineState["MEMORY"][address] = machineState["MEMORY"][address] >> 1

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical shift right on {hex(address)}")

    machineState["PC"] += 2


def opcode_48(machineState: dict):
    #PHA IMPLIED 1 3
    address = 0x0100 + machineState["SP"]
    machineState["MEMORY"][address] = machineState["ACC"]
    machineState["SP"] -= 1

    if config.VERBOSE:
        print(f"Pushed accumulator ({bin(machineState['ACC'])} to stack)")

    machineState["PC"] += 1


def opcode_49(machineState: dict):
    #EOR IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_4a(machineState: dict):
    #LSR ACCUM 1 2

    if machineState["ACC"] & 0b1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    machineState["ACC"] = machineState["ACC"] >> 1

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical shift right of ACC")

    machineState["PC"] += 1

def opcode_4c(machineState: dict):
    #JMP ABS 3 3
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    machineState["PC"] = address

    if config.VERBOSE:
        print(f"Jumped to {hex(address)}")

def opcode_4d(machineState: dict):
    #EOR ABS 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3

def opcode_4e(machineState: dict):
    #LSR ABS 3 6
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])

    if machineState["MEMORY"][address] & 0b1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    machineState["MEMORY"][address] = machineState["MEMORY"][address] >> 1

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical shift right on {hex(address)}")

    machineState["PC"] += 3


def opcode_50(machineState: dict):
    #BVC Relative 2 2


    if machineState["FLAGS"] & 0b01000000 == 0b00000000:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 2
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because carry flag was clear")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because carry flag was not clear")



def opcode_51(machineState: dict):
    #EOR (IND),Y 2 5

    address = machineState["MEMORY"][machineState["PC"] + 1]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte])) + machineState["Y"]
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2


def opcode_55(machineState: dict):
    #EOR ZP,X 2 4

    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical OR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2



def opcode_56(machineState: dict):
    #LSR ZP,X 2 6
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]

    if machineState["MEMORY"][address] & 0b1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    machineState["MEMORY"][address] = machineState["MEMORY"][address] >> 1

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical shift right on {hex(address)}")

    machineState["PC"] += 2

def opcode_58(machineState: dict):
    #CLI Implied 1 2

    machineState["FLAGS"] = machineState["FLAGS"] & 0b11111011

    if config.VERBOSE:
        print(f"Cleared Interrupt flag")

    machineState["PC"] += 1


def opcode_59(machineState: dict):
    #EOR ABS,Y 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["Y"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3


def opcode_5d(machineState: dict):
    #EOR ABS,X 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] = machineState["ACC"] ^ data

    if machineState["ACC"] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical XOR ACC with {hex(data)} (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3



def opcode_5e(machineState: dict):
    #LSR ABS,X 3 7

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]

    if machineState["MEMORY"][address] & 0b1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    machineState["MEMORY"][address] = machineState["MEMORY"][address] >> 1

    if machineState["MEMORY"][address] == 0b00000000:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Logical shift right on {hex(address)}")

    machineState["PC"] += 3


def opcode_60(machineState: dict):
    #RTS Implied 1 6

    #pull pc from stack
    #inc SP
    pc = 0
    machineState["SP"] += 1
    pc += machineState["MEMORY"][0x0100 + machineState["SP"]]
    machineState["SP"] += 1
    pc += machineState["MEMORY"][0x0100 + machineState["SP"]] << 8

    machineState["PC"] = pc

    if config.VERBOSE:
        print(f"Returned from subroutine to {hex(pc)}")

def opcode_61(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_65(machineState: dict):
    #ADC (ZP) 2 3
    data = machineState["MEMORY"][machineState["MEMORY"][machineState["PC"]+1]]
    machineState["ACC"] += data

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"{hex(data)} added to ACC (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2



def opcode_66(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_68(machineState: dict):
    #PLA IMPLIED 1 4


    machineState["SP"] += 1
    address = 0x0100 + machineState["SP"]
    machineState["ACC"] = machineState["MEMORY"][address]

    if config.VERBOSE:
        print(f"Pulled stack to accumulator ({bin(machineState['ACC'])})")

    machineState["PC"] += 1



def opcode_69(machineState: dict):
    #ADC IMM 2 2
    data = machineState["MEMORY"][machineState["PC"]+1]
    machineState["ACC"] += data

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"{hex(data)} added to ACC (now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_6a(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_6c(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_6d(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_6e(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_70(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_71(machineState: dict):
    #ADC (Indirect),Y 2 5

    address = machineState["MEMORY"][machineState["PC"] + 1]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte])) + machineState["Y"]
    data = machineState["MEMORY"][newAddress]

    machineState["ACC"] += data + (machineState["FLAGS"] & 0b00000001)

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Performed ADC on ACC (Now {hex(machineState['ACC'])})")

    machineState["PC"] += 2

def opcode_75(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_76(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_78(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_79(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_7d(machineState: dict):
    #ADC ABS,X 3 2
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]
    data = machineState["MEMORY"][address]

    machineState["ACC"] += data

    if machineState["ACC"] > 0xff: #carry flag
        machineState["ACC"] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"{hex(data)} added to ACC (now {hex(machineState['ACC'])})")

    machineState["PC"] += 3

def opcode_7e(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_81(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_84(machineState: dict):
    #STY (ZP) 2 3

    address = machineState["MEMORY"][machineState["PC"]+1]
    machineState["MEMORY"][address] = machineState["Y"]

    if config.VERBOSE:
        print(f"Stored Y into memory at {hex(address)}")

    machineState["PC"] += 2


def opcode_85(machineState: dict):
    #STA (ZP) 2 3

    address = machineState["MEMORY"][machineState["PC"]+1]
    machineState["MEMORY"][address] = machineState["ACC"]

    if config.VERBOSE:
        print(f"Stored ACC into memory at {hex(address)}")

    machineState["PC"] += 2

def opcode_86(machineState: dict):
    #STX (ZP) 2 3

    address = machineState["MEMORY"][machineState["PC"]+1]
    machineState["MEMORY"][address] = machineState["X"]

    if config.VERBOSE:
        print(f"Stored X into memory at {hex(address)}")

    machineState["PC"] += 2

def opcode_88(machineState: dict):
    #DEY Implied 1 2
    machineState["Y"] -= 1
    
    if machineState["Y"] < 0:
        machineState["Y"] += 0x100

    if machineState["Y"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["Y"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Decremented Y to {hex(machineState['Y'])}")

    machineState["PC"] += 1


def opcode_8a(machineState: dict):
    #TXA Implied 1 2
    machineState["ACC"] = machineState["X"]

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Moved X ({hex(machineState['X'])}) to ACC")

    machineState["PC"] += 1

def opcode_8c(machineState: dict):
    #STY ABS 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    machineState["MEMORY"][address] = machineState["Y"]

    if config.VERBOSE:
        print(f"Stored Y into memory at {hex(address)}")

    machineState["PC"] += 3

def opcode_8d(machineState: dict):
    #STA ABS 3 4
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    machineState["MEMORY"][address] = machineState["ACC"]
    if config.VERBOSE:
        print(f"Stored ACC into memory at {hex(address)}")

    machineState["PC"] += 3

def opcode_8e(machineState: dict):
    #STX ABS 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    machineState["MEMORY"][address] = machineState["X"]

    if config.VERBOSE:
        print(f"Stored X into memory at {hex(address)}")

    machineState["PC"] += 3


def opcode_90(machineState: dict):
    #BCC Relative 2 2

    if machineState["FLAGS"] & 0b00000001 == 0b00000000:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 2
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because carry flag was clear (relative jump by {decOffset})")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because carry flag was not clear")

def opcode_91(machineState: dict):
    #STA (IND),Y 2 6

    address = machineState["MEMORY"][machineState["PC"] + 1]
    dereferenced = machineState["MEMORY"][address]
    newAddress = dereferenced + machineState["Y"]

    machineState["MEMORY"][newAddress] = machineState["ACC"]

    if config.VERBOSE:
        print(f"Stored ACC at address {hex(newAddress)}")

    machineState["PC"] += 2




def opcode_94(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_95(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_96(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_98(machineState: dict):
    #TYA IMPLIED 1 2
    machineState["ACC"] = machineState["Y"]

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Moved Y ({hex(machineState['Y'])}) to ACC")

    machineState["PC"] += 1


def opcode_99(machineState: dict):
    #STA ABS,Y 3 5
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["Y"]

    machineState["MEMORY"][address] = machineState["ACC"]

    if config.VERBOSE:
        print(f"Wrote to ram at address {hex(address)}: {hex(machineState['ACC'])}")

    machineState["PC"] += 3


def opcode_9a(machineState: dict):
    #TXS Implied 1 2
    machineState["SP"] = machineState["X"]

    if config.VERBOSE:
        print(f"Transferred X register to stack pointer")

    machineState["PC"] += 1

def opcode_9d(machineState: dict):
    #STA ABS,X 3 5
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]

    machineState["MEMORY"][address] = machineState["ACC"]

    if config.VERBOSE:
        print(f"Wrote to ram at address {hex(address)}: {hex(machineState['ACC'])}")

    machineState["PC"] += 3

def opcode_a0(machineState: dict):
    #LDY IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]
    machineState["Y"] = data

    if machineState["Y"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["Y"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Loaded {hex(data)} into Y")

    machineState["PC"] += 2

def opcode_a1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_a2(machineState: dict):
    #LDX IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]
    machineState["X"] = data

    if machineState["X"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["X"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Loaded {hex(data)} into X")

    machineState["PC"] += 2

def opcode_a4(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_a5(machineState: dict):
    #LDA ZP 2 3

    data = machineState["MEMORY"][machineState["MEMORY"][machineState["PC"]+1]]
    machineState["ACC"] = data

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Loaded {hex(data)} into ACC")

    machineState["PC"] += 2

def opcode_a6(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_a8(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_a9(machineState: dict):
    # LDA IMM 2 2
    data = machineState["MEMORY"][machineState["PC"]+1]
    machineState["ACC"] = data

    if config.VERBOSE:
        print(f"Loaded {hex(data)} into ACC")

    machineState["PC"] += 2

def opcode_aa(machineState: dict):
    #TAX Implied 1 2
    data = machineState["ACC"]
    machineState["X"] = data

    if config.VERBOSE:
        print(f"Set X to ACC ({hex(data)})")

    machineState["PC"] += 1

def opcode_ac(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ad(machineState: dict):
    #LDA ABS 3 4

    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]
    machineState["ACC"] = data

    if config.VERBOSE:
        print(f"Loaded {hex(data)} into ACC")

    machineState["PC"] += 3

def opcode_ae(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_b0(machineState: dict):
    #BCS Rel 2 2
    if machineState["FLAGS"] & 0b00000001 == 0b00000001:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 2
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because carry flag was set (relative jump by {decOffset})")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because carry flag was clear")

def opcode_b1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_b4(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_b5(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_b6(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_b8(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_b9(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ba(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_bc(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_bd(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_be(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_c0(machineState: dict):
    #CPY IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]

    if machineState["Y"] >= data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["Y"] == data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if (machineState["Y"] - data) & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Compared Y ({hex(machineState['Y'])}) to {hex(data)}")

    machineState["PC"] += 2

def opcode_c1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_c4(machineState: dict):
    #CPY ZP 2 3

    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]

    if machineState["Y"] >= data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["Y"] == data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if (machineState["Y"] - data) & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Compared Y ({hex(machineState['Y'])}) to {hex(data)}")

    machineState["PC"] += 2



def opcode_c5(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_c6(machineState: dict):
    #DEC ZP 2 5
    address = machineState["MEMORY"][machineState["PC"] + 1]
    machineState["MEMORY"][address] -= 1

    if machineState["MEMORY"][address] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["MEMORY"][address] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Decremented memory at {hex(address)}")

    machineState["PC"] += 2

def opcode_c8(machineState: dict):
    #INY IMPLIED 1 2
    machineState["Y"] += 1

    if machineState["Y"] > 0xff:
        machineState["Y"] -= 0x100

    if machineState["Y"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["Y"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Incremented Y (to {hex(machineState['Y'])})")

    machineState["PC"] += 1

def opcode_c9(machineState: dict):
    #CMP Immidiate 2 2

    data = machineState["MEMORY"][machineState["PC"] + 1]

    if machineState["ACC"] >= data: #carry flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["ACC"] == data: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if (machineState["ACC"]-data) & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Compared ACC to {hex(data)}")

    machineState["PC"] += 2


def opcode_ca(machineState: dict):
    #DEX Implied 1 2

    machineState["X"] -= 1
    if machineState["X"] < 0:
        machineState["X"] += 0x100

    if machineState["X"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["X"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Decremented X (to {hex(machineState['X'])})")

    machineState["PC"] += 1



def opcode_cc(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_cd(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ce(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_d0(machineState: dict):
    #BNE Relative 2 2

    if machineState["FLAGS"] & 0b00000010 == 0b00000000:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 2
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because zero flag was clear (relative jump by {decOffset})")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because zero flag was not clear")


def opcode_d1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_d5(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_d6(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_d8(machineState: dict):
    #CLD Implied 1 2

    machineState["FLAGS"] = machineState["FLAGS"] & 0b11110111

    if config.VERBOSE:
        print(f"Cleared Decimal flag")

    machineState["PC"] += 1


def opcode_d9(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_dd(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_de(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_e0(machineState: dict):
    #CPX IMM 2 2
    data = machineState["MEMORY"][machineState["PC"] + 1]

    if machineState["X"] >= data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110

    if machineState["X"] == data:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if (machineState["X"] - data) & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Compared X ({hex(machineState['X'])}) to {hex(data)}")

    machineState["PC"] += 2

def opcode_e1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_e4(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_e5(machineState: dict):
    #SBC ZP 2 3

    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]

    AccBit7 = (machineState["ACC"] & 0b10000000) >> 7
    DataBit7 = (data & 0b10000000) >> 7

    C = machineState["FLAGS"] & 0b00000001
    machineState["ACC"] = machineState["ACC"] - data - (1-C)

    ResBit7 = (machineState["ACC"] & 0b10000000) >> 7

    if machineState["ACC"] < 0x00:
        machineState["ACC"] += 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001

    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111  

    if ResBit7 == 1 and AccBit7 == 0 and DataBit7 == 0:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b01000000
    elif ResBit7 == 0 and AccBit7 == 1 and DataBit7 == 1:
        machineState["FLAGS"] = machineState["FLAGS"] | 0b01000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b10111111

    if config.VERBOSE:
        print(f"Subtracted {hex(data)} from acc (now {machineState['ACC']})")

    machineState["PC"] += 2

    

def opcode_e6(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_e8(machineState: dict):
    #INX Implied 1 2
    machineState["X"] += 1

    if machineState["X"] > 0xff:
        machineState["X"] -= 0x100

    if machineState["X"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101

    if machineState["X"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111

    if config.VERBOSE:
        print(f"Incremented X (to {hex(machineState['X'])})")

    machineState["PC"] += 1

def opcode_e9(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ea(machineState: dict):
    #NOP implied 1 2
    if config.VERBOSE:
        print("NOP")

    machineState["PC"] += 1

def opcode_ec(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ed(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_ee(machineState: dict):
    Crash(machineState, "Instruction not implemented")


def opcode_f0(machineState: dict):
    #BEQ Rel 2 2
    if machineState["FLAGS"] & 0b00000010 == 0b00000010:
        offset = machineState["MEMORY"][machineState["PC"] + 1]
        if offset & 0b10000000 == 0b10000000:
            #offset is negative
            decOffset = offset - 256
        else:
            decOffset = offset
        machineState["PC"] += decOffset + 2
        if config.VERBOSE:
            print(f"Jumped to {hex(machineState['PC'])} because zero flag was set (relative jump by {decOffset})")
    else:
        machineState["PC"] += 2
        if config.VERBOSE:
            print(f"Hit jump, but didnt jump because zero flag was clear")

def opcode_f1(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_f5(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_f6(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_f8(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_f9(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_fd(machineState: dict):
    Crash(machineState, "Instruction not implemented")

def opcode_fe(machineState: dict):
    Crash(machineState, "Instruction not implemented")

"""
This dictionary contains all opcodes, indexed by their numerical value. for example, the opcode for ORA (IND,X) is 0x01, 
and the opcode can be executed by calling the function at the key 0x02 in the dictionary
"""
switch_table = {
    0x00: opcode_00,
    0x01: opcode_01,
    0x05: opcode_05,
    0x06: opcode_06,
    0x08: opcode_08,
    0x09: opcode_09,
    0x0a: opcode_0a,
    0x0d: opcode_0d,
    0x0e: opcode_0e,

    0x10: opcode_10,
    0x11: opcode_11,
    0x15: opcode_15,
    0x16: opcode_16,
    0x18: opcode_18,
    0x19: opcode_19,
    0x1d: opcode_1d,
    0x1e: opcode_1e,

    0x20: opcode_20,
    0x21: opcode_21,
    0x24: opcode_24,
    0x25: opcode_25,
    0x26: opcode_26,
    0x28: opcode_28,
    0x29: opcode_29,
    0x2a: opcode_2a,
    0x2c: opcode_2c,
    0x2d: opcode_2d,
    0x2e: opcode_2e,

    0x30: opcode_30,
    0x31: opcode_31,
    0x35: opcode_35,
    0x36: opcode_36,
    0x38: opcode_38,
    0x39: opcode_39,
    0x3d: opcode_3d,
    0x3e: opcode_3e,

    0x40: opcode_40,
    0x41: opcode_41,
    0x45: opcode_45,
    0x46: opcode_46,
    0x48: opcode_48,
    0x49: opcode_49,
    0x4a: opcode_4a,
    0x4c: opcode_4c,
    0x4d: opcode_4d,
    0x4e: opcode_4e,

    0x50: opcode_50,
    0x51: opcode_51,
    0x55: opcode_55,
    0x56: opcode_56,
    0x58: opcode_58,
    0x59: opcode_59,
    0x5d: opcode_5d,
    0x5e: opcode_5e,

    0x60: opcode_60,
    0x61: opcode_61,
    0x65: opcode_65,
    0x66: opcode_66,
    0x68: opcode_68,
    0x69: opcode_69,
    0x6a: opcode_6a,
    0x6c: opcode_6c,
    0x6d: opcode_6d,
    0x6e: opcode_6e,

    0x70: opcode_70,
    0x71: opcode_71,
    0x75: opcode_75,
    0x76: opcode_76,
    0x78: opcode_78,
    0x79: opcode_79,
    0x7d: opcode_7d,
    0x7e: opcode_7e,

    0x81: opcode_81,
    0x84: opcode_84,
    0x85: opcode_85,
    0x86: opcode_86,
    0x88: opcode_88,
    0x8a: opcode_8a,
    0x8c: opcode_8c,
    0x8d: opcode_8d,
    0x8e: opcode_8e,

    0x90: opcode_90,
    0x91: opcode_91,
    0x94: opcode_94,
    0x95: opcode_95,
    0x96: opcode_96,
    0x98: opcode_98,
    0x99: opcode_99,
    0x9a: opcode_9a,
    0x9d: opcode_9d,

    0xa0: opcode_a0,
    0xa1: opcode_a1,
    0xa2: opcode_a2,
    0xa4: opcode_a4,
    0xa5: opcode_a5,
    0xa6: opcode_a6,
    0xa8: opcode_a8,
    0xa9: opcode_a9,
    0xaa: opcode_aa,
    0xac: opcode_ac,
    0xad: opcode_ad,
    0xae: opcode_ae,

    0xb0: opcode_b0,
    0xb1: opcode_b1,
    0xb4: opcode_b4,
    0xb5: opcode_b5,
    0xb6: opcode_b6,
    0xb8: opcode_b8,
    0xb9: opcode_b9,
    0xba: opcode_ba,
    0xbc: opcode_bc,
    0xbd: opcode_bd,
    0xbe: opcode_be,

    0xc0: opcode_c0,
    0xc1: opcode_c1,
    0xc4: opcode_c4,
    0xc5: opcode_c5,
    0xc6: opcode_c6,
    0xc8: opcode_c8,
    0xc9: opcode_c9,
    0xca: opcode_ca,
    0xcc: opcode_cc,
    0xcd: opcode_cd,
    0xce: opcode_ce,

    0xd0: opcode_d0,
    0xd1: opcode_d1,
    0xd5: opcode_d5,
    0xd6: opcode_d6,
    0xd8: opcode_d8,
    0xd9: opcode_d9,
    0xdd: opcode_dd,
    0xde: opcode_de,

    0xe0: opcode_e0,
    0xe1: opcode_e1,
    0xe4: opcode_e4,
    0xe5: opcode_e5,
    0xe6: opcode_e6,
    0xe8: opcode_e8,
    0xe9: opcode_e9,
    0xea: opcode_ea,
    0xec: opcode_ec,
    0xed: opcode_ed,
    0xee: opcode_ee,

    0xf0: opcode_f0,
    0xf1: opcode_f1,
    0xf5: opcode_f5,
    0xf6: opcode_f6,
    0xf8: opcode_f8,
    0xf9: opcode_f9,
    0xfd: opcode_fd,
    0xfe: opcode_fe
}

#7582 ♥