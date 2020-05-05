import pygame
import sys

# game settings
WIDTH = 1024
HEIGHT = 768
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 60
TITLE = 'GRID'
BGCOLOR = (255, 255, 255)  # dark grey

TILE_SIZE = 32
GRIDWIDTH = (int)(WIDTH / TILE_SIZE)
GRIDHEIGHT = (int)(HEIGHT / TILE_SIZE)


class Node:
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.rect = (self.x, self.y, self.size, self.size)
        self.color = (0, 0, 0)
        self.width = 1
        self.screen = surface

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.width)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(BGCOLOR)

    for y in range(GRIDHEIGHT):
        for x in range(GRIDWIDTH):
            n = Node(x * 32, y * 32, screen)
            n.draw()

    while (True):
        for event in pygame.event.get():
            if (event.type) == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                print('it\'s down')

            if (event.type == pygame.MOUSEBUTTONUP):
                print('it\'s up')

        pygame.display.update()


if __name__ == "__main__":
    main()
