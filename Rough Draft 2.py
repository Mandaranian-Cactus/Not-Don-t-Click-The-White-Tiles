import pygame
import sys
import random

class Window:
    def __init__(self, w, h, block_w):
        self.w_idx = w
        self.h_idx = h
        self.w = w * block_w
        self.h = h * block_w
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.grid = [[0 for i in range(w)] for i in range(h)]
        self.block_w = block_w
        self.opacity_grid = [[[1, 0] for i in range(w)] for i in range(h)]  # Adds shading-in effect

    def fill(self):
        self.screen.fill((255, 255, 255))

    def draw_grid(self):
        for y in range(self.h_idx):
            for x in range(self.w_idx):
                # White Tile
                # if self.grid[y][x] == 0:
                #     # Draw shape
                #     color = self.opacity_grid[y][x][0] * 255
                #     pygame.draw.rect(self.screen, (color, color, color), (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

                # # Black Tile
                # if self.grid[y][x] == 1:

                    # Change opacity
                if self.opacity_grid[y][x][1] == -1:
                        self.opacity_grid[y][x][0] = max(0, self.opacity_grid[y][x][0] - 0.03)
                        if self.opacity_grid[y][x][0] == 0:
                            self.opacity_grid[y][x][1] = 0
                elif self.opacity_grid[y][x][1] == 1:
                        self.opacity_grid[y][x][0] = min(1, self.opacity_grid[y][x][0] + 0.1)
                        if self.opacity_grid[y][x][0] == 1:
                            self.opacity_grid[y][x][1] = 0
                            # self.grid[y][x] = 0

                # Draw shape
                color = self.opacity_grid[y][x][0] * 255
                pygame.draw.rect(self.screen, (color, color, color), (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Horizontal lines
        for y in range(self.h_idx):
            pygame.draw.line(self.screen, (135,135,135), (0, y * self.block_w), (self.w, y * self.block_w))

        # Vertical Lines
        for x in range(self.w_idx):
            pygame.draw.line(self.screen, (135,135,135), (x * self.block_w, 0), (x * self.block_w, self.h))

    def gen_black_tile(self):
        while True:
            x = random.randrange(0, self.w_idx)
            y = random.randrange(0, self.h_idx)

            if self.grid[y][x] == 0:  # Check to see if tile is available (Not being used/covered)
                self.grid[y][x] = 1
                self.opacity_grid[y][x][0] = 1
                self.opacity_grid[y][x][1] = -1
                break

screen = Window(4, 4, 173)
# screen = Window(4, 4, 75)
pygame.init()
clock = pygame.time.Clock()

for i in range(3):
    screen.gen_black_tile()

while True:
    screen.fill()
    screen.draw_grid()

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // screen.block_w  # Convert to index format
            y = y // screen.block_w  # Convert to index format
            if screen.grid[y][x]:
                # Click was valid
                screen.gen_black_tile()  # Do this before to ensure that we don't fill the same block again
                screen.grid[y][x] = 0
                screen.opacity_grid[y][x][1] = 1

                # print(*screen.opacity_grid, sep ='\n', end ='\n\n')

            else:
                # Click was not valid
                print("reset")
                exec(open("Rough Draft 2.py").read())


    pygame.display.update()
    clock.tick(70)  # Fps (Don't know why/how it does it)