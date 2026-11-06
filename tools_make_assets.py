from struct import pack
import os

def bmp(path, w, h, color=(20,20,35), border=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = (w * 3 + 3) & ~3
    size = 54 + row * h
    data = bytearray()
    data += b'BM'
    data += pack('<IHHI', size, 0, 0, 54)
    data += pack('<IiiHHIIiiII', 40, w, h, 1, 24, 0, row*h, 2835, 2835, 0, 0)
    for y in range(h):
        line = bytearray()
        for x in range(w):
            c = color
            if border and (x < 2 or y < 2 or x >= w-2 or y >= h-2):
                c = border
            line += bytes((c[2], c[1], c[0]))
        line += b'\x00' * (row - w*3)
        data += line
    open(path, 'wb').write(data)

bmp("assets/backgrounds/title_top.bmp", 256, 192, (10,10,28))
bmp("assets/backgrounds/title_bottom.bmp", 256, 192, (18,18,38))
bmp("assets/ui/menu_box.bmp", 220, 120, (32,24,55), (210,180,80))
bmp("assets/ui/button.bmp", 160, 24, (40,34,70), (210,180,80))
bmp("assets/ui/selector.bmp", 170, 24, (80,60,20), (255,220,90))
bmp("assets/cursor/cursor.bmp", 16, 16, (255,0,255), (255,220,90))
bmp("assets/cards/card_back.bmp", 32, 48, (40,30,80), (180,140,60))
bmp("assets/cards/empty_slot.bmp", 32, 48, (18,18,24), (90,90,110))
