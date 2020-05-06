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

    # getter function for f_cost
    @property
    def f_cost(self):
        return self.h_cost + self.g_cost

    def show(self):
        if self.mode == 'default':
            pygame.draw.rect(screen, COLOR_BLACK, (self.x * TILE_SIZE,
                                                   self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        if self.mode == 'obstacle':
            pygame.draw.rect(screen, COLOR_GREY, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        if self.mode == 'open':
            pygame.draw.rect(screen, COLOR_GREEN, (self.x * TILE_SIZE,
                                                   self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

        if self.mode == 'closed':
            pygame.draw.rect(screen, COLOR_RED, (self.x * TILE_SIZE,
                                                 self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        if self.mode == 'start' or self.mode == 'end' or self.mode == 'path':
            pygame.draw.rect(screen, COLOR_BLUE, (self.x * TILE_SIZE,
                                                  self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

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
    dist_x = abs(node_a.x - node_b.x)
    dist_y = abs(node_a.y - node_b.y)
    return (dist_x > dist_y) if 1.4 * dist_y + (dist_x - dist_y) else 1.4 * dist_x + (dist_y - dist_x)

# create start and end points
start_node = grid[5][5]
start_node.mode = 'start'
start_node.show()
end_node = grid[30][45]
end_node.mode = 'end'
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

# first render of grid
show_grid()

while not done:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not start:
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()

        if pygame.key.get_pressed()[K_SPACE]:
            start = True

        elif pygame.key.get_pressed()[K_s] and pygame.mouse.get_pressed()[0]:
            # todo
            continue

        elif pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, c, = y // TILE_SIZE, x // TILE_SIZE
            grid[r][c].mode = 'obstacle'
            grid[r][c].show()

    current_node = open_set[0]

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




# while True:
#     # clock.tick(60)
#     # display grid
#     # show_grid()

#     events = pygame.event.get()
#     # pygame.display.update()

#     # run path finding algorithm
#     if pygame.key.get_pressed()[K_SPACE]:
#         pathfinding(start_pos, end_pos)

#     for ev in events:
#         if ev.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # select start node
#     if pygame.key.get_pressed()[K_s] and pygame.mouse.get_pressed()[0]:
#         x, y = pygame.mouse.get_pos()
#         r, c, = y // TILE_SIZE, x // TILE_SIZE
#         grid[r][c].is_source = True
#         start_node = grid[r][c]

#     # select end node
#     elif pygame.key.get_pressed()[K_e] and pygame.mouse.get_pressed()[0]:
#         x, y = pygame.mouse.get_pos()
#         r, c, = y // TILE_SIZE, x // TILE_SIZE
#         grid[r][c].is_target = True
#         end_node = grid[r][c]

#     # checks for left mouse down. (left, scroll, right): boolean
#     elif pygame.mouse.get_pressed()[0]:
#         position = pygame.mouse.get_pos()  # returns (x,y)
#         # draw_obstacle(position)

#         x, y = position
#         # map to grids
#         r, c, = y // TILE_SIZE, x // TILE_SIZE
#         grid[r][c].show_obstacle()

#     pygame.display.update()


# if __name__ == "__main__":
#     main()
