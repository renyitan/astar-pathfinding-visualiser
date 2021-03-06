import pygame
from pygame import *
from math import sqrt
import sys

import map_1  # custom map

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
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('')

clock = pygame.time.Clock()
screen.fill(COLOR_WHITE)


class Node:
    def __init__(self, i, j):
        self.x = j
        self.y = i
        self.mode = 'default'

        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

        # strict mode, for start/end nodes so that the node color does not change
        self.strict = False

    # getter function for f_cost
    @property
    def f_cost(self):
        return self.h_cost + self.g_cost

    def show(self):
        if self.strict:
            pygame.draw.rect(screen, COLOR_BLUE, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        elif self.mode == 'default':
            pygame.draw.rect(screen, COLOR_WHITE, (self.x * TILE_SIZE,
                                                   self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, COLOR_BLACK, (self.x * TILE_SIZE,
                                                   self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        elif self.mode == 'obstacle':
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        elif self.mode == 'open':
            pygame.draw.rect(screen, COLOR_GREEN, (self.x * TILE_SIZE,
                                                   self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        elif self.mode == 'closed':
            pygame.draw.rect(screen, COLOR_RED, (self.x * TILE_SIZE,
                                                 self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        elif self.mode == 'start' or self.mode == 'end' or self.mode == 'path':
            pygame.draw.rect(screen, COLOR_BLUE, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


# Create grid 2d array; grid[row][col]
grid = [[0 for i in range(NUM_ROWS)] for j in range(NUM_COLS)]

# fill grid with empty Tile
for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
        grid[i][j] = Node(i, j)

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
    return sqrt((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2)


# create start and end points
start_node = grid[5][45]
start_node.mode, start_node.strict = 'start', True
start_node.show()
end_node = grid[30][5]
end_node.mode, end_node.strict = 'end', True
end_node.show()

open_set = []   # set of nodes to be evaluated
closed_set = []  # set of node already evaluated

done = False
num = 0

# delay
doOnce = 0
start = False

# open_set.append(start_node)
open_set.append(start_node)


def print_map():
    map = [[0 for i in range(NUM_ROWS)] for j in range(NUM_COLS)]
    for x in range(NUM_ROWS):
        for y in range(NUM_COLS):
            if grid[x][y].mode == 'obstacle':
                map[x][y] = 1
    return map


def load_map(map_file):
    if len(map_file.map) != NUM_ROWS:
        print('Map not the right size')
        return

    for i in range(map_file.NUM_ROWS):
        for j in range(map_file.NUM_COLS):
            if map_file.map[i][j] == 1:
                grid[i][j].mode = 'obstacle'


# first render of grid
show_grid()

while not done:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pressed = pygame.mouse.get_pressed()
    if not start:
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()

        if pygame.key.get_pressed()[K_SPACE]:
            start = True

        elif pygame.key.get_pressed()[K_s] and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE

            old_start = start_node
            old_start.mode, old_start.strict = 'default', False
            old_start.show()

            start_node = grid[r][c]
            start_node.mode, start_node.strict = 'start', True
            start_node.show()

            open_set.append(start_node)
            open_set.remove(old_start)

        elif pygame.key.get_pressed()[K_e] and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE

            old_end = end_node
            old_end.mode, old_end.strict = 'default', False
            old_end.show()

            end_node = grid[r][c]
            end_node.mode, end_node.strict = 'end', True
            end_node.show()

        elif pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE
            grid[r][c].mode = 'obstacle'
            grid[r][c].show()

        elif pygame.key.get_pressed()[K_p]:
            map = print_map()
            print(map)

        elif pygame.key.get_pressed()[K_l]:
            load_map(map_1)
            show_grid()

    current_node = open_set[0]

    # for interactive mode, draw obstacle while algo is running. 
    # if pygame.mouse.get_pressed()[0]:
    #     x, y = pygame.mouse.get_pos()
    #     r, c, = y // TILE_SIZE, x // TILE_SIZE
    #     grid[r][c].mode = 'obstacle'
    #     grid[r][c].show()

    if start:

        if (len(open_set)) == 0:
            break

        show_grid()

        # look for node with lowest f_cost
        for i in range(len(open_set)):
            if open_set[i].f_cost < current_node.f_cost or (open_set[i].f_cost == current_node.f_cost and open_set[i].h_cost < current_node.h_cost):
                current_node = open_set[i]
                current_node.mode = 'open'

        open_set.remove(current_node)
        current_node.mode = 'closed'
        closed_set.append(current_node)

        if current_node == end_node:
            done = True

        for neighbour in get_neighbours(current_node):
            if neighbour.mode == 'obstacle' or neighbour in closed_set:
                continue

            movement_cost = current_node.g_cost + \
                get_distance(current_node, neighbour)
            if movement_cost < neighbour.g_cost or neighbour not in open_set:
                neighbour.g_cost = movement_cost
                neighbour.h_cost = get_distance(neighbour, end_node)
                neighbour.parent = current_node
            if neighbour not in open_set:
                neighbour.mode = 'open'
                open_set.append(neighbour)

    pygame.display.update()
    clock.tick(FPS)


def retrace_path():
    paths = []
    current_node = end_node
    while current_node is not start_node:
        paths.append(current_node)
        current_node = current_node.parent

    paths.reverse()
    return paths


paths = retrace_path()

# reset grids


def reset_grid():
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if grid[i][j].mode == 'obstacle':
                continue
            else:
                grid[i][j].mode = 'default'


reset_grid()

while True:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for path in paths:
        path.mode = 'path'

    show_grid()

    pygame.display.update()
    clock.tick(FPS)
