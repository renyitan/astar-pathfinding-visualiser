import pygame
from pygame import *
import sys

# game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
TITLE = 'GRID'

TILE_SIZE = 16
NUM_COLS = SCREEN_WIDTH // TILE_SIZE
NUM_ROWS = SCREEN_HEIGHT // TILE_SIZE

# color constants
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (40, 40, 40)

# initialisation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(COLOR_WHITE)


class Tile:

    def __init__(self, row, col):
        self.x = col
        self.y = row
        self.is_obstacle = False
        self.is_source = False
        self.is_target = False
        self.color = COLOR_BLACK  # default color
        self.t_type = 1  # default, no fill

    def show(self):
        if self.is_obstacle:
            self.color, self.t_type = COLOR_GREY, 0
        elif self.is_target or self.is_source:
            self.color, self.t_type = COLOR_BLUE, 0
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE,
                                              self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), self.t_type)


# Create grid 2d array; grid[row][col]
grid = [[0 for i in range(NUM_ROWS)] for j in range(NUM_COLS)]
# fill grid with empty Tile
for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
        grid[i][j] = Tile(i, j)

# set screen borders as obstacles
for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
        grid[0][j].is_obstacle = True
        grid[NUM_ROWS-1][j].is_obstacle = True
    grid[i][0].is_obstacle = True
    grid[i][NUM_COLS-1].is_obstacle = True


def show_grid():
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            grid[i][j].show()


def draw_obstacle(position):
    x, y = position
    # map to grids
    r, c, = y // TILE_SIZE, x // TILE_SIZE
    selected_tile = grid[r][c]
    selected_tile.is_obstacle = True


def main():
    pygame.init()

    start_node = (0, 0)
    end_node = (0,0)

    while (True):

        # display grid
        show_grid()

        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # select start node
            if pygame.key.get_pressed()[K_s] and pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                r, c, = y // TILE_SIZE, x // TILE_SIZE
                grid[r][c].is_source = True
                start_node = (r,c)

            # select end node
            elif pygame.key.get_pressed()[K_e] and pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                r, c, = y // TILE_SIZE, x // TILE_SIZE
                grid[r][c].is_target = True
                end_node = (r,c)


            # checks for left mouse down. (left, scroll, right): boolean
            elif pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()  # returns (x,y)
                draw_obstacle(position)

        pygame.display.update()


if __name__ == "__main__":
    main()
