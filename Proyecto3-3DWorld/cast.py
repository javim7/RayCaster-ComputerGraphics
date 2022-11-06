import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)


pygame.init()
screen = pygame.display.set_mode((500, 500))

r = Raycaster(screen)

running = True
while running:
    x = random.randint(0, 500)
    y = random.randint(0, 500)
    r.point(x, y)

    pygame.display.flip()

    for event in pygame.event.get():
        if (event. type == pygame.QUIT):
            running = False
