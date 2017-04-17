import pygame
import math
import sys
from threading import Thread



class GPU:

    def __init__(self, memory):

        # Start the display
        pygame.init()
        self.screen = pygame.display.set_mode([160,144])
        self.background = pygame.Surface((256,256))
        self.background.fill((175,200,70))
        self.white = (175, 200, 70 , 255)
        self.light_grey = (130, 170, 100, 255)
        self.dark_grey = (35, 110, 95, 255)
        self.black = (10, 40, 85, 255)
        self.cycles = 0
        self.memory = memory
        self.counter = 0

    def update(self, cycles_passed):

        self.cycles += cycles_passed

        LY = int(self.cycles / 456)
        if LY > 153: LY = 153
        self.memory.write(0xFF44, LY)

        # Vblank period begin
        if LY == 0x90:
            #
            self.counter += 1
        else:
            self.counter += 1

        # 70220 clock cycles is one frame
        if self.cycles >= 70220:
            self.cycles = 0
            self.render_background()
            for event in pygame.event.get():
            	if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

    def render_background(self):

        # Initialized the background
        self.background_pixels = pygame.PixelArray(self.background)

        # Read each byte at BG Map Data 1
        for index in range(0, 0x400):

            tile_choice = self.memory.read(0x9800 + index)

            # Tile data is 16 bytes long
            tile_data_index = self.memory.read(0x8000 + tile_choice * 16)

            # Get each portion of the tile data in increments of 2 bytes (a row at a time)
            rows = [[],[],[],[],[],[],[],[]]
            for i in range(0,16,2):
                byte1 = self.memory.read(0x8000 + tile_data_index + i)
                byte2 = self.memory.read(0x8000 + tile_data_index + i + 1)

                # Determine the color of each pixel (2 bits), example:
                # byte1 = 0b10001111
                # byte2 = 0b01101001
                # colors = [0x10, 0x01, 0x01, 0x00, 0x11, 0x10, 0x10, 0x11]
                colors = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
                for b in range(0,8):

                    c1 = byte1 & (0x80 >> b)
                    c2 = byte2 & (0x80 >> b)

                    if c1: c1 = 1
                    else: c1 = 0
                    if c2: c2 = 1
                    else: c2 = 0

                    s = (c2 << 1) | c1
                    if s == 0:
                        color = self.white
                    elif s == 1:
                        color = self.light_grey
                    elif s == 2:
                        color = self.dark_grey
                    elif s == 3:
                        color = self.black
                    else:
                        color = (255,0,0) # bad tiles are red
                    colors[b] = color

                rows[int(i/2)] = colors

            # Copy each row from the tile into the background array
            for y in range(0,8):
                for x in range(0,8):
                    xindex = (index % 32) * 8 + x
                    yindex = int(index / 32) * 8 + y
                    self.background_pixels[xindex, yindex] = rows[y][x]

        del self.background_pixels
        gpu_thread = Thread(target=self.render)
        gpu_thread.start()




    def render(self):

        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
