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

    def __init__(self, i, j):
        self.x = j
        self.y = i
        self.is_obstacle = False
        self.is_source = False
        self.is_target = False
        self.color = COLOR_BLACK  # default color
        self.t_type = 1  # default, no fill

        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    # getter function for f_cost
    @property
    def f_cost(self):
        return self.h_cost + self.g_cost

    def show(self):
        if self.is_obstacle:
            self.color, self.t_type = COLOR_GREY, 0
        elif self.is_target or self.is_source:
            self.color, self.t_type = COLOR_BLUE, 0
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE,
                                              self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), self.t_type)

    def show_open(self):
        pygame.draw.rect(screen, COLOR_GREEN, (self.x * TILE_SIZE,
                                               self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

    def show_closed(self):
        pygame.draw.rect(screen, COLOR_RED, (self.x * TILE_SIZE,
                                             self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

    def show_path(self):
        pygame.draw.rect(screen, COLOR_BLUE, (self.x * TILE_SIZE,
                                              self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    
    def show_obstacle(self):
        self.is_obstacle = True
        pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                              self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        


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

show_grid()

def draw_obstacle(position):
    x, y = position
    # map to grids
    r, c, = y // TILE_SIZE, x // TILE_SIZE
    selected_tile = grid[r][c]
    selected_tile.is_obstacle = True


def get_neighbours(node):
    neighbours = []
    for x in range(-1, 2):  # -1,0,1
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            # checking the peripheral nodes
            check_x, check_y = node.x + x, node.y + y
            if check_x >= 0 and check_x < NUM_COLS and check_y >= 0 and check_y < NUM_ROWS:
                neighbours.append(grid[check_y][check_x])

    return neighbours


def get_distance(node_a, node_b):
    dist_x = abs(node_a.x - node_b.x)
    dist_y = abs(node_a.y - node_b.y)

    if dist_x > dist_y:
        return 1.4 * dist_y + (dist_x - dist_y)
    else:
        return 1.4 * dist_x + (dist_y - dist_x)


def retrace_path(start_node, end_node):
    path = []
    current_node = end_node
    while current_node is not start_node:
        path.append(current_node)
        current_node = current_node.parent

    path.reverse()
    draw_path(path)


def draw_path(path):
    for p in path:
        p.show_path()


def pathfinding(start_node, end_node):
    open_set = []   # set of nodes to be evaluated
    closed_set = []  # set of node already evaluated

    open_set.append(start_node)

    while (len(open_set) > 0):
        current_node = open_set[0]

        # search for the node with the lowest f_cost
        for i in range(len(open_set)):
            if open_set[i].f_cost < current_node.f_cost or (open_set[i].f_cost == current_node.f_cost and open_set[i].h_cost < current_node.h_cost):
                current_node = open_set[i]
                current_node.is_opened = True

        open_set.remove(current_node)
        closed_set.append(current_node)
        current_node.show_closed()

        if current_node == end_node:
            retrace_path(start_node, end_node)
            return

        for neighbour in get_neighbours(current_node):
            if neighbour.is_obstacle or neighbour in closed_set:
                continue

            movement_cost = current_node.g_cost + \
                get_distance(current_node, neighbour)
            if movement_cost < neighbour.g_cost or neighbour not in open_set:
                neighbour.g_cost = movement_cost
                neighbour.h_cost = get_distance(neighbour, end_node)
                neighbour.parent = current_node

            if neighbour not in open_set:
                open_set.append(neighbour)
                neighbour.show_open()

        # for node in open_set:
        #     node.show_open()
        #     pygame.display.flip()

        # for node in closed_set:
        #     node.show_closed()
        #     pygame.display.flip()


clock = pygame.time.Clock()


def main():
    pygame.init()

    start_pos = grid[5][5]
    end_pos = grid[23][28]


    while True:
        clock.tick(60)
        # display grid
        # show_grid()

        events = pygame.event.get()
        # pygame.display.update()

        # run path finding algorithm
        if pygame.key.get_pressed()[K_SPACE]:
            pathfinding(start_pos, end_pos)

        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # select start node
        if pygame.key.get_pressed()[K_s] and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE
            grid[r][c].is_source = True
            start_node = grid[r][c]

        # select end node
        elif pygame.key.get_pressed()[K_e] and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE
            grid[r][c].is_target = True
            end_node = grid[r][c]

        # checks for left mouse down. (left, scroll, right): boolean
        elif pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()  # returns (x,y)
            # draw_obstacle(position)

            x, y = position
            # map to grids
            r, c, = y // TILE_SIZE, x // TILE_SIZE
            grid[r][c].show_obstacle()

        pygame.display.update()


if __name__ == "__main__":
    main()
