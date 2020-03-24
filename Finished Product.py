import pygame
import sys
import random
import time as sleep_mode
from collections import deque


class Window:
    def __init__(self, w, h, block_w, fps):
        self.w_idx = w
        self.h_idx = h
        self.w = w * block_w
        self.h = h * block_w
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.fps = fps

    def fill(self):
        self.screen.fill((255, 255, 255))


class Play_Grid:
    def __init__(self, w, h, block_w, combo_bar_w, combo_bar_h, combo_bar_x, combo_bar_y, time_limit):
        self.w_idx = w  # Width in indexes
        self.h_idx = h  # Height in indexes
        self.w = w * block_w  # Width in pixels
        self.h = h * block_w  # Height in pixels
        self.grid = [[0 for i in range(w)] for i in range(h)]  # Bool 2-D array holding info about what tiles are black a.k.a active and which are not
        self.block_w = block_w  # Length of each index/block_width in pixels
        # Below line adds shading in/out effects
        # In the form [opacity (0-1),  change option (1 = icnrease opacity, 0 = dont change opacity, -1 = decrease opacity), (target Red, target Blue, target Green)]
        self.opacity_grid = [[[1, 0, [255, 255, 255]] for i in range(w)] for i in range(h)]
        self.uber_mode_bool = False  # Toggle for uber mode
        self.uber_mode_cnt = 0  # The number of blocks removed during uber mode (Uber mode if turned off when the player has clicked all tiles on screen)
        self.temp_score = 0  # Temp score regulates the # of correct clicks to trigger the "Add time" function
        self.score = 0  # Tracks the permanent score / total # of correct clicks
        self.frame_cnt = 0  # Helps regulate when a second has passed

        self.combo_bar_x = combo_bar_x
        self.combo_bar_y = combo_bar_y
        self.combo_bar_w = combo_bar_w
        self.combo_bar_h = combo_bar_h
        self.combo_bar_amt = 0  # Current amt in bar
        self.combo_bar_limit = 100  # Max limit of bar

        self.time = time_limit  # Time left on counter (Triggers a restart of the program)
        self.reset_flag = False  # Used to trigger a reset of program

    def change_opacity(self, x, y):
        # Change opacity
        if self.opacity_grid[y][x][1] == -1:  # More Black
            self.opacity_grid[y][x][0], color = self.decrease_opacity(self.opacity_grid[y][x][0], (255, 255, 255))
            if self.opacity_grid[y][x][0] == 0:
                # Shade in effect is complete
                self.opacity_grid[y][x][1] = 0

        elif self.opacity_grid[y][x][1] == 1:  # More White
            self.opacity_grid[y][x][0], color = self.increase_opacity(self.opacity_grid[y][x][0], (77, 255, 77))
            if self.opacity_grid[y][x][0] == 1:
                # Shade out effect is complete
                self.opacity_grid[y][x][1] = 0

        elif self.opacity_grid[y][x][1] == 0:
            color = self.opacity_grid[y][x][0] * 255, self.opacity_grid[y][x][0] * 255, self.opacity_grid[y][x][0] * 255

        return color

    def draw_grid(self):

        # Draw individual tiles
        for y in range(self.h_idx):
            for x in range(self.w_idx):
                color = self.change_opacity(x, y)
                pygame.draw.rect(screen.screen, color, (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Horizontal lines
        for y in range(self.h_idx + 1):
            pygame.draw.line(screen.screen, (175, 175, 175), (0, y * self.block_w), (self.w, y * self.block_w))

        # Vertical Lines
        for x in range(self.w_idx + 1):
            pygame.draw.line(screen.screen, (175, 175, 175), (x * self.block_w, 0), (x * self.block_w, self.h))

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
        self.combo_bar_amt = min(self.combo_bar_amt + 4.5, 100)  # 3

    def combo_bar_decrease(self):
        self.combo_bar_amt = max(self.combo_bar_amt - 0.12, 0)  # 0.12

    def combo_bar_draw(self):
        # Draw Background bar (Centered)
        pygame.draw.rect(screen.screen, (29, 109, 138), (self.combo_bar_x - self.combo_bar_w / 2,
                                                         self.combo_bar_y - self.combo_bar_h / 2,
                                                         self.combo_bar_w,
                                                         self.combo_bar_h))
        # Draw Active bar (Centered)
        pygame.draw.rect(screen.screen, (252, 126, 126), (self.combo_bar_x - self.combo_bar_w / 2,
                                                          self.combo_bar_y - self.combo_bar_h / 2,
                                                          self.combo_bar_w * (
                                                                      self.combo_bar_amt / self.combo_bar_limit),
                                                          self.combo_bar_h))

    def initiate_uber_mode(self):
        for y in range(self.h_idx):
            for x in range(self.w_idx):
                self.grid[y][x] = 1  # Set block to be active
                self.opacity_grid[y][x][0] = 1  # Set block opacity to be max (white)
                self.opacity_grid[y][x][1] = -1  # Set opacity change to be a decrease (Makes the shad in effect from white to black)


class Text_display:

    # Note that class has 1 major drawback where any limited duration texts need to be in seconds (Done for slight optimization reasons)

    def __init__(self, time_left, score):
        self.temp_queue = deque()  # Texts with finite duration
        self.perm_queue = deque()  # Texts with infinite duration

        # Note that both of these variables are in the form [txt, (xPos, yPos)]
        self.time_left = time_left  # text specifically for the time left
        self.score = score  # Text specifically for the score

    def draw(self):
        # Draw temp_queue
        for i in range(len(self.temp_queue)):
            txt_info = self.temp_queue.popleft()
            txt, pos, duration = txt_info
            screen.screen.blit(txt, pos)

            self.temp_queue.append([txt, pos, duration])

        # Draw perm_queue
        for i in range(len(self.perm_queue)):
            txt_info = self.perm_queue.popleft()
            txt, pos = txt_info
            screen.screen.blit(txt, pos)

            self.perm_queue.append([txt, pos])

        # Draw time left and score
        screen.screen.blit(self.time_left[0], self.time_left[1])
        screen.screen.blit(self.score[0], self.score[1])

    def check_duration(self):  # Check duration left on all texts
        for i in range(len(self.temp_queue)):
            txt_info = self.temp_queue.popleft()
            txt, pos, duration = txt_info

            if duration <= 0:
                continue  # Prevents any appending
            duration -= 1

            self.temp_queue.append([txt, pos, duration])  # Text has yet to end so we re-append it back into the queue


def update():

    # Check to see if player has clicked enough block to have more time given
    if game.temp_score % 20 == 0 and game.temp_score > 0:
        game.temp_score = 0
        game.time += 10  # Add time onto the counter

    # Take 1 second away from time counter
    if game.frame_cnt % screen.fps == 0 and game.frame_cnt > 0:
        game.frame_cnt = 0  # Frame count regulates how long it takes for a second to pass
        game.time -= 1
        text_display.time_left[0] = font.render(str(game.time), False, (0, 0, 0))  # Change the in-game timer value
        text_display.check_duration()  # Check to see if any texts have exceeded their time limit

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check to exit game
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()  # Get coordinate format
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

                    text_display.score[0] = font.render(str(game.score), False, (0, 0, 0))  # Increase the score counter

                    if game.uber_mode_bool:  # Used to regulate and check when to exit uber-mode
                        game.uber_mode_cnt += 1

                        if game.uber_mode_cnt == game.w_idx * game.h_idx:  # Case for exiting uber mode
                            # If all uber mode blocks have been clicked, turn uber mode off and reset all uber mode settings
                            game.uber_mode_bool = False  # Turn off uber-mode.
                            game.uber_mode_cnt = 0

                            # Basically restart the game by generating 3 block tiles randomly
                            for i in range(3):
                                game.gen_black_tile()

                    if game.combo_bar_amt == game.combo_bar_limit:  # Check is combo meter is ready
                        # Initiate uber mode
                        game.uber_mode_bool = True
                        game.initiate_uber_mode()
                        text_display.temp_queue.append([pygame.font.SysFont('Comic Sans MS', 60).
                                                       render("Uber Mode", False, (255, 195, 77)),
                                                        [game.w / 2 - 150, game.h / 2 - 45], 1])
                        game.combo_bar_amt = 0

                else:
                    # Click was not valid
                    game.reset_flag = True

            except IndexError:  # Used to catch mouse clicks that are outside of the 4 x 4 grid (Such as accidentally
                # tapping on combo bar)
                pass

    # Time limit exceeded
    if game.time == 0:  # Further investigation needed on why it has to be -1 and not 0
        print("reset", game.score)
        exec(open("Rough Draft 8.py").read())

    # Click on white tile
    if game.reset_flag:
        color = [255, 120, 122]
        # Color the given tile red
        pygame.draw.rect(screen.screen, color,
                         (x * game.block_w, y * game.block_w, game.block_w, game.block_w))

        pygame.display.update()  # Update screen to show the red tile
        sleep_mode.sleep(0.1)  # Give some time for the player to recognize the red tile
        print("reset", game.score)
        exec(open("Rough Draft 8.py").read())  # Restart

    game.combo_bar_decrease()  # Decrease combo bar
    game.frame_cnt += 1  # Increase frame count


def draw():
    screen.fill()
    game.draw_grid()
    game.combo_bar_draw()
    text_display.draw()

    pygame.display.update()
    clock.tick(screen.fps)  # Fps (Don't know why/how it does it)


screen = Window(4, 5, 173, 70)
game = Play_Grid(4, 4, 173, 400, 20, screen.w / 2, 800, 10)
pygame.init()  # Initiate module
pygame.font.init()  # Initiate module
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)  # Set up font
text_display = Text_display([font.render(str(game.time), False, (0, 0, 0)), (600, 775)],
                            [font.render(str(game.score), False, (0, 0, 0)), (60, 775)])
# Note that the duration for which the message is on screen is based off of seconds
text_display.perm_queue.append([font.render("Time", False, (0, 0, 0)), (580, 730)])
text_display.perm_queue.append([font.render("Score", False, (0, 0, 0)), (42, 730)])

# Start with adding 3 random black tiles
for i in range(3):
    game.gen_black_tile()

while True:
    update()
    draw()

