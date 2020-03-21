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

    def fill(self):
        self.screen.fill((255, 255, 255))

class Play_Grid:
    def __init__(self, w, h, block_w, combo_bar_w, combo_bar_h, combo_bar_x, combo_bar_y):
        self.w_idx = w
        self.h_idx = h
        self.w = w * block_w
        self.h = h * block_w
        self.grid = [[0 for i in range(w)] for i in range(h)]
        self.block_w = block_w
        self.opacity_grid = [[[1, 0] for i in range(w)] for i in range(h)]  # Adds shading-in effect

        self.combo_bar_x = combo_bar_x
        self.combo_bar_y = combo_bar_y
        self.combo_bar_w = combo_bar_w
        self.combo_bar_h = combo_bar_h
        self.combo_bar_amt = 0
        self.combo_bar_limit = 100

    def draw_grid(self):
        for y in range(self.h_idx):
            for x in range(self.w_idx):

                # Change opacity
                if self.opacity_grid[y][x][1] == -1:
                    self.opacity_grid[y][x][0] = max(0, self.opacity_grid[y][x][0] - 0.03)
                    if self.opacity_grid[y][x][0] == 0:
                        self.opacity_grid[y][x][1] = 0
                elif self.opacity_grid[y][x][1] == 1:
                    self.opacity_grid[y][x][0] = min(1, self.opacity_grid[y][x][0] + 0.08)
                    if self.opacity_grid[y][x][0] == 1:
                        self.opacity_grid[y][x][1] = 0

                # Draw shape
                color = self.opacity_grid[y][x][0] * 255
                pygame.draw.rect(screen.screen, (color, color, color), (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Horizontal lines
        for y in range(self.h_idx + 1):
            pygame.draw.line(screen.screen, (175,175,175), (0, y * self.block_w), (self.w, y * self.block_w))

        # Vertical Lines
        for x in range(self.w_idx + 1):
            pygame.draw.line(screen.screen, (175,175,175), (x * self.block_w, 0), (x * self.block_w, self.h))

    def gen_black_tile(self):
        while True:
            x = random.randrange(0, self.w_idx)
            y = random.randrange(0, self.h_idx)

            if self.grid[y][x] == 0:  # Check to see if tile is available (Not being used/covered)
                self.grid[y][x] = 1
                self.opacity_grid[y][x][0] = 1
                self.opacity_grid[y][x][1] = -1
                break

    def combo_bar_increase(self):
        self.combo_bar_amt = min(self.combo_bar_amt + 3, 100)

    def combo_bar_decrease(self):
        self.combo_bar_amt = max(self.combo_bar_amt - 0.12, 0)

    def combo_bar_draw(self):
        # Draw Background bar
        pygame.draw.rect(screen.screen, (29, 109, 138), (self.combo_bar_x - self.combo_bar_w / 2,
                                                         self.combo_bar_y - self.combo_bar_h / 2,
                                                         self.combo_bar_w,
                                                         self.combo_bar_h))
        # Draw Active bar
        pygame.draw.rect(screen.screen, (252, 126, 126), (self.combo_bar_x - self.combo_bar_w / 2,
                                                          self.combo_bar_y - self.combo_bar_h / 2,
                                                          self.combo_bar_w * (self.combo_bar_amt / self.combo_bar_limit),
                                                          self.combo_bar_h))



screen = Window(4, 5, 173)
game = Play_Grid(4, 4, 173, 400, 20, screen.w / 2, 800)
pygame.init()
clock = pygame.time.Clock()
score = 0

for i in range(3):
    game.gen_black_tile()

while True:
    screen.fill()
    game.draw_grid()
    game.combo_bar_decrease()
    game.combo_bar_draw()

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x or event.key == pygame.K_z:
                x, y = pygame.mouse.get_pos()
                x = x // game.block_w  # Convert to index format
                y = y // game.block_w  # Convert to index format

                try:
                    if game.grid[y][x]:
                        # Click was valid
                        game.gen_black_tile()  # Do this before to ensure that we don't fill the same block again
                        game.grid[y][x] = 0  # Set that block to be open
                        game.opacity_grid[y][x][1] = 1 # Set block to slowly shade off screen
                        game.combo_bar_increase()
                        score += 1

                    else:
                        # Click was not valid
                        print("reset", score)
                        exec(open("Rough Draft 3.py").read())

                except IndexError:  # Used to catch mouse clicks that are outside of the 4 x 4 grid (Such as accidentally
                                    # tapping on combo bar)
                    pass




    pygame.display.update()
    clock.tick(70)  # Fps (Don't know why/how it does it)