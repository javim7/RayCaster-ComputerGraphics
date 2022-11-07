import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

colors = [
    (0, 0, 0),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.blockSize = 50
        self.map = []
        self.player = {
            "x": int(self.blockSize + self.blockSize / 2),
            "y": int(self.blockSize + self.blockSize / 2),
        }

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, c=WHITE):
        for i in range(x, x + self.blockSize + 1):
            for j in range(y, y + self.blockSize + 1):
                self.point(i, j, c)

    def loadMap(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

        print(self.map)

    def drawMap(self):
        for x in range(0, 500, self.blockSize):
            for y in range(0, 500, self.blockSize):
                i = int(x / self.blockSize)
                j = int(y / self.blockSize)
                if self.map[j][i] != ' ':
                    self.block(x, y, colors[int(self.map[j][i])])

    def drawPlayer(self):
        self.point(self.player["x"], self.player["y"], WHITE)

    def render(self):
        self.drawMap()
        self.drawPlayer()


pygame.init()
screen = pygame.display.set_mode((500, 500))

r = Raycaster(screen)
r.loadMap('./Proyecto3-3DWorld/map.txt')

running = True
while running:
    r.render()

    pygame.display.flip()

    for event in pygame.event.get():
        if (event. type == pygame.QUIT):
            running = False
