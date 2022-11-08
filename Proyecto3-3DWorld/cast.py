import pygame
import random
from math import cos, sin, pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY = (50, 100, 200)
GROUND = (100, 200, 100)

colors = [
    (0, 20, 10),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
    (21, 42, 138),
]

walls = {
    "1": pygame.image.load('./Proyecto3-3DWorld/wall1.png'),
    "2": pygame.image.load('./Proyecto3-3DWorld/wall2.png'),
    "3": pygame.image.load('./Proyecto3-3DWorld/wall3.png'),
    "4": pygame.image.load('./Proyecto3-3DWorld/wall4.png'),
    "5": pygame.image.load('./Proyecto3-3DWorld/wall5.png'),
}


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.blockSize = 50
        self.map = []
        self.player = {
            "x": int(self.blockSize + self.blockSize / 2),
            "y": int(self.blockSize + self.blockSize / 2),
            "fov": int(pi/3),
            "a": int(pi/3),
        }

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blockSize):
            for j in range(y, y + self.blockSize):
                tx = int((i - x) * 128 / self.blockSize)
                ty = int((j - y) * 128 / self.blockSize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def loadMap(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def castRay(self, a):
        d = 0
        ox = self.player['x']
        oy = self.player['y']

        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x/self.blockSize)
            j = int(y/self.blockSize)

            if self.map[j][i] != ' ':
                hitx = x - i * self.blockSize
                hity = y - j * self.blockSize

                if 1 < hitx < self.blockSize-1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blockSize)
                return d, self.map[j][i], tx

            self.point(x, y)
            d += 1

    def drawMap(self):
        for x in range(0, 500, self.blockSize):
            for y in range(0, 500, self.blockSize):
                i = int(x / self.blockSize)
                j = int(y / self.blockSize)
                if self.map[j][i] != ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def drawStake(self, x, h, c, tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

    def drawPlayer(self):
        self.point(self.player["x"], self.player["y"], WHITE)

    def render(self):
        self.drawMap()
        self.drawPlayer()

        density = 100

        # minimapa
        for i in range(0, density):
            a = self.player['a'] - self.player['fov'] / \
                2 + self.player['fov'] * i / density
            d, c, tx = self.castRay(a)

        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)

        # dibujar en 3d
        density = 100
        for i in range(0, int(self.width/2)):
            a = self.player['a'] - self.player['fov'] / \
                2 + self.player['fov'] * i / (self.width/2)
            d, c, tx = self.castRay(a)

            x = int(self.width/2) + i
            h = (self.height / (d*cos(a - self.player['a']))) * self.height/10

            self.drawStake(x, h, c, tx)


pygame.init()
screen = pygame.display.set_mode((1000, 500))

r = Raycaster(screen)
r.loadMap('./Proyecto3-3DWorld/map.txt')

running = True
while running:
    screen.fill(BLACK, (0, 0, r.width/2, r.height/2))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))

    r.render()

    pygame.display.flip()

    for event in pygame.event.get():
        if (event. type == pygame.QUIT):
            running = False

        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_a:
                r.player["a"] -= pi/25
            if event.key == pygame.K_d:
                r.player["a"] += pi/25

            if event.key == pygame.K_RIGHT:
                r.player["x"] += 5
            if event.key == pygame.K_LEFT:
                r.player["x"] -= 5
            if event.key == pygame.K_UP:
                r.player["y"] -= 5
            if event.key == pygame.K_DOWN:
                r.player["y"] += 5
