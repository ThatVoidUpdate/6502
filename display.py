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
}

class Display:
    def __init__(self):
        self.screen = graphics.GraphWin("Memory view", 32*8, 32*8)
        self.screenRects = []
        self.oldScreenMemory = [0]*(0x600-0x200)
        for y in range(0, 32):
            for x in range(0, 32):
                colour = colours[0]
                rect = graphics.Rectangle(graphics.Point(x*8, y*8), graphics.Point((x+1)*8, (y+1)*8))
                rect.setFill(colour)
                rect.setOutline(colour)
                rect.draw(self.screen)
                self.screenRects.append(rect)

    def UpdateScreen(self, machineState: list):
        screenMemory = machineState["MEMORY"][0x200:0x600]
        for y in range(0, 32):
            for x in range(0, 32):
                if screenMemory[y*32+x] != self.oldScreenMemory[y*32+x]:
                    value = screenMemory[y * 32 + x] % 16
                    colour = colours[value]

                    self.screenRects[y*32+x].setFill(colour)
                    self.screenRects[y*32+x].setOutline(colour)
        self.oldScreenMemory = screenMemory

    def Quit(self):
        self.screen.close()