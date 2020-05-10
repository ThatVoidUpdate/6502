"""
A program to generate the binary data for the character set.
Each character is expressed as 8 hex numbers, witheach one being the hex of the binary representation of the row of pixels
For example, if the top row of a character was "  XX X X", that would be 00110101 in binary, or 0x35, meaning that 0x35 would be stored for the first row of the character
"""
from PIL import Image

img = Image.open("Charset.png").convert("RGB") #Load the image and convert to RGB
data = img.load() #Load the image data
size = img.size #Get the image size
outputData = []
for y in range(0, size[1], 8):
    for x in range(0, size[0], 8): #For every character in the image
        for line in range(0, 8): #For every line of that character
            lineData = 0
            for bit in range(0, 8): #For every bit in that line
                value = data[x+bit, y+line] #Get the pixel value
                lineData = (lineData << 1) + (1 if value == (0, 0, 0) else 0) #And shift it into the binary number
            #print(hex(lineData), end=", ")
            outputData.append(lineData) #Append the number to the file
#print(outputData)
with open("characterRom.bin", "wb") as outputFile:
    outputFile.write(bytearray(outputData)) #Write the binary file
                