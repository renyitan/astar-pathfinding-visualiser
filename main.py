import pygame
import sys

# game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
TITLE = 'GRID'

TILE_SIZE = 16
NUM_COLS = (int)(SCREEN_WIDTH / TILE_SIZE)
NUM_ROWS = (int)(SCREEN_HEIGHT / TILE_SIZE)

# color constants
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (211, 211, 211)

# initialisation
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(COLOR_WHITE)


class Tile:
    def __init__(self, row, col):
        self.x = col
        self.y = row
        self.is_obstacle = False  #
        self.color = COLOR_BLACK  # default color
        self.t_type = 1  # default, no fill

    def show(self):
        if self.is_obstacle:
            self.color = COLOR_GREY
            self.t_type = 0

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

def main():
    pygame.init()

    while (True):

        # display grid
        show_grid()

        events = pygame.event.get()

        for ev in events:
            if (ev.type) == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # checks for left mouse down. (left, scroll, right): boolean
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                print(position)

        pygame.display.update()


if __name__ == "__main__":
    main()
