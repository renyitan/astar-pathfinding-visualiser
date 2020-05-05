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





def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(BGCOLOR)

    for y in range(GRIDHEIGHT):
        for x in range(GRIDWIDTH):
            pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
            

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
