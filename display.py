import graphics

class Display:
    def __init__(self):
        self.screen = graphics.GraphWin("Memory view", 32*8, 32*8)
        self.screenRects = []
        self.oldScreenMemory = [0]*(0x600-0x200)
        for y in range(0, 32):
            for x in range(0, 32):
                value = 0
                colour = graphics.color_rgb(value, value, value)
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
                    value = screenMemory[y * 32 + x] * 16
                    colour = graphics.color_rgb(value, value, value)

                    self.screenRects[y*32+x].setFill(colour)
                    self.screenRects[y*32+x].setOutline(colour)
                    #self.screenRects[y*32+x].draw(self.screen)
        self.oldScreenMemory = screenMemory

    def Quit(self):
        self.screen.close()