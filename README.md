# 6502

# TODO
check exactly how BRK works, I may have implemented it wrong

# Example Implementation
To make it easier to test, I have attached a graphical display to the cpu, and mapped some memory locations

Memory map:
0x0000 - 0x00FF : Free Ram
0x0100 - 0x01FF : Stack
0x0200 - 0x05FF : Screen Memory
0x0600 - 0x7FFF : Free Ram
0x8000 - 0xFFF9 : Rom
0xFFFA - 0xFFFB : NMI Vector
0xFFFC - 0xFFFD : Reset Vector
0xFFFE - 0xFFFF : IRQ Vector