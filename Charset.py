from PIL import Image

img = Image.open("Charset.png").convert("RGB")
data = img.load()
size = img.size
for y in range(0, size[1], 8):
    for x in range(0, size[0], 8):
        for line in range(0, 8):
            lineData = 0
            for bit in range(0, 8):
                value = data[x+bit, y+line]
                lineData = (lineData << 1) + (1 if value == (0, 0, 0) else 0)
            print(hex(lineData), end=", ")
                