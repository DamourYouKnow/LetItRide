import sys
import pygame

if __name__ == '__main__':
    print("MATH 3808 Final Project")

    pygame.init()
    screen = pygame.display.set_mode((800, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
