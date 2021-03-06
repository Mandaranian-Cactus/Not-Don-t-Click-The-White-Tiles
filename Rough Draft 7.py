import pygame
import sys
import random
import time as sleep_mode

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
        self.opacity_grid = [[[1, 0, [255, 255, 255]] for i in range(w)] for i in range(h)]  # Adds shading-in effect
        self.uber_mode_bool = False
        self.uber_mode_cnt = 0  # The number of blocks removed during uber mode (Uber mode if turned off when the player has clicked all tiles on screen)
        self.score = 0
        self.temp_score = 0

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
                if self.opacity_grid[y][x][1] == -1:  # More Black
                    self.opacity_grid[y][x][0], color = self.decrease_opacity(self.opacity_grid[y][x][0], (255, 255, 255))
                    if self.opacity_grid[y][x][0] == 0:
                        self.opacity_grid[y][x][1] = 0

                elif self.opacity_grid[y][x][1] == 1:  # More White
                    self.opacity_grid[y][x][0], color = self.increase_opacity(self.opacity_grid[y][x][0], (77, 255, 77))
                    if self.opacity_grid[y][x][0] == 1:
                        self.opacity_grid[y][x][1] = 0

                elif self.opacity_grid[y][x][1] == 0:
                    color = self.opacity_grid[y][x][0] * 255, self.opacity_grid[y][x][0] * 255, self.opacity_grid[y][x][0] * 255

                # Draw shape
                pygame.draw.rect(screen.screen, color, (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Horizontal lines
        for y in range(self.h_idx + 1):
            pygame.draw.line(screen.screen, (175,175,175), (0, y * self.block_w), (self.w, y * self.block_w))

        # Vertical Lines
        for x in range(self.w_idx + 1):
            pygame.draw.line(screen.screen, (175,175,175), (x * self.block_w, 0), (x * self.block_w, self.h))

    def increase_opacity(self, opacity, lower_limit):  # Assume that max is (255, 255, 255) a.k.a white
        new_color = (lower_limit[0] + opacity * (255 - lower_limit[0]),
                     lower_limit[1] + opacity * (255 - lower_limit[1]),
                     lower_limit[2] + opacity * (255 - lower_limit[2]))
        opacity = min(1, opacity + 0.05)
        return opacity, new_color

    def decrease_opacity(self, opacity, higher_limit):  # Assumes that min is (0, 0, 0) a.k.a black
        new_color = (opacity * higher_limit[0],
                     opacity * higher_limit[1],
                     opacity * higher_limit[2])
        opacity = max(0, opacity - 0.035)
        return opacity, new_color

    def gen_black_tile(self):

        if self.uber_mode_bool:  # If uber mode is on, we don't generate any new black tiles
            return

        while True:
            # Note that the x and y are indexes on the grid and not coordinates
            x = random.randrange(0, self.w_idx)
            y = random.randrange(0, self.h_idx)

            if self.grid[y][x] == 0:  # Check to see if tile is available (Not being used/covered)
                self.grid[y][x] = 1  # Mark block as being occupied
                self.opacity_grid[y][x][0] = 1  # Set opacity to be max (White)
                self.opacity_grid[y][x][1] = -1  # Set to have opacity decrease / become more black
                break

    def combo_bar_increase(self):
        self.combo_bar_amt = min(self.combo_bar_amt + 3, 100)  # 3

    def combo_bar_decrease(self):
        self.combo_bar_amt = max(self.combo_bar_amt - 0.12, 0)  # 0.12

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

    def initiate_uber_mode(self):
        for y in range(self.h_idx):
            for x in range(self.w_idx):
                self.grid[y][x] = 1
                self.opacity_grid[y][x][0] = 1
                self.opacity_grid[y][x][1] = -1


screen = Window(4, 5, 173)
game = Play_Grid(4, 4, 173, 400, 20, screen.w / 2, 800)
pygame.init()
clock = pygame.time.Clock()
time = 10
frame_cnt = 0
reset_flag = False

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
font = pygame.font.SysFont('Comic Sans MS', 30)


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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // game.block_w  # Convert to index format
            y = y // game.block_w  # Convert to index format

            try:
                if game.grid[y][x]:
                    # Click was valid
                    game.gen_black_tile()  # Do this before to ensure that we don't fill the same block again
                    game.grid[y][x] = 0  # Set that block to be open
                    game.opacity_grid[y][x][1] = 1  # Set block to slowly shade off screen
                    game.combo_bar_increase()
                    game.score += 1
                    game.temp_score += 1

                    if game.uber_mode_bool:
                        game.uber_mode_cnt += 1

                        if game.uber_mode_cnt == game.w_idx * game.h_idx:
                            # If all uber mode blocks have been clicked, turn uber mode off and reset all uber mode settings
                            game.uber_mode_bool = False
                            game.uber_mode_cnt = 0

                            for i in range(3):
                                game.gen_black_tile()

                    if game.combo_bar_amt == game.combo_bar_limit:  # Check is combo meter is ready
                        # Initiate uber mode
                        game.uber_mode_bool = True
                        game.initiate_uber_mode()
                        game.combo_bar_amt = 0

                else:
                    # Click was not valid
                    reset_flag = True

            except IndexError:  # Used to catch mouse clicks that are outside of the 4 x 4 grid (Such as accidentally
                                # tapping on combo bar)
                pass

    if game.temp_score % 40 == 0 and game.temp_score > 0:
        game.temp_score = 0
        time += 10

    if frame_cnt % 70 == 0:
        frame_cnt = 0

        time_txt = font.render(str(time), False, (0, 0, 0))
        time -= 1

    score_txt = font.render(str(game.score), False, (0, 0, 0))
    screen.screen.blit(score_txt, (75, 775))
    screen.screen.blit(time_txt, (600, 775))
    frame_cnt -= 1

    if time == -1:  # Further investigation needed on why it has to be -1 and not 0
        print("reset", game.score)
        exec(open("Rough Draft 7.py").read())

    if reset_flag:
        color = [255, 120, 122]
        pygame.draw.rect(screen.screen, color,
                         (x * game.block_w, y * game.block_w, game.block_w, game.block_w))

        pygame.display.update()
        sleep_mode.sleep(0.1)
        print("reset", game.score)
        exec(open("Rough Draft 7.py").read())

    pygame.display.update()
    clock.tick(70)  # Fps (Don't know why/how it does it)

