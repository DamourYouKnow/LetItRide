import sys
from screen import MainMenu
import pygame

if __name__ == '__main__':
    print("MATH 3808 Final Project")

    pygame.init()
    canvas = pygame.display.set_mode((800, 500))
    screen = MainMenu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            screen.handle(event)
        screen.update()
        screen.draw(canvas)
        pygame.display.flip()
        screen = screen.next()
