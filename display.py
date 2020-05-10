"""
Am example implementation of a display for the 6502.
This code uses the graphics.py library for a simple way to display graphics
"""
import graphics

colours = {
    0x0: graphics.color_rgb(0, 0, 0),
    0x1: graphics.color_rgb(0, 0, 128),
    0x2: graphics.color_rgb(0, 128, 0),
    0x3: graphics.color_rgb(0, 128, 128),
    0x4: graphics.color_rgb(128, 0, 0),
    0x5: graphics.color_rgb(128, 0, 128),
    0x6: graphics.color_rgb(128, 128, 0),
    0x7: graphics.color_rgb(192, 192, 192),
    0x8: graphics.color_rgb(128, 128, 128),
    0x9: graphics.color_rgb(0, 0, 255),
    0xa: graphics.color_rgb(0, 255, 0),
    0xb: graphics.color_rgb(0, 255, 255),
    0xc: graphics.color_rgb(255, 0, 0),
    0xd: graphics.color_rgb(255, 0, 255),
    0xe: graphics.color_rgb(255, 255, 0),
    0xf: graphics.color_rgb(255, 255, 255),
} #A list of colours that can be displayed


#32 x 32 screen = 1024 bytes of screen ram
#256 bytes of character rom

class Display:
    def __init__(self):
        self.screen = graphics.GraphWin("Memory view", 32*8, 32*8) #Initialise the window
        self.oldScreenMemory = [0]*(0x600-0x200) #Create an empty list for the old memory, so that i dont redraw things that havent changed
        colour = colours[0]
        rect = graphics.Rectangle(graphics.Point(0, 0), graphics.Point(32*8, 32*8))
        rect.setFill(colour)
        rect.setOutline(colour)
        rect.draw(self.screen) #Cover the window in black

    def UpdateScreen(self, machineState: list):
        screenMemory = machineState["MEMORY"][0x200:0x600] #Get the memory that is assigned to the screen

        for y in range(0, 32):
            for x in range(0, 32): #For every character on the screen
                if screenMemory[y*32+x] != self.oldScreenMemory[y*32+x]: #If the data has changed
                    CharacterOffset = screenMemory[y * 32 + x] * 8 #Get the offset to the character in character rom

                    for line in range(8): 
                        data = machineState["MEMORY"][0x8000 + CharacterOffset + line]
                        for i in range(8):
                            bit = data >> (8-i) & 1 #For every bit in the character

                            if bit == 1: #Draw it
                                self.screen.plotPixel(x * 8 + i, y * 8 + line, color="white")
                            else:
                                self.screen.plotPixel(x * 8 + i, y * 8 + line, color="black")

        self.oldScreenMemory = screenMemory #Update the old memory

    def Quit(self):
        self.screen.close()