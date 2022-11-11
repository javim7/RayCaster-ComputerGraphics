import pygame
from math import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (152, 0, 136)
SKY = (50, 100, 200)
GROUND = (200, 200, 100)

colors = [
    (0, 20, 10),
    (4, 91, 82),
    (219, 242, 38),
    (0, 0, 255),
    (255, 255, 255)
]

walls = {
    "1": pygame.image.load('./Proyecto3-3DWorld/wall1.png'),
    "2": pygame.image.load('./Proyecto3-3DWorld/wall2.png'),
    "3": pygame.image.load('./Proyecto3-3DWorld/wall3.png'),
    "4": pygame.image.load('./Proyecto3-3DWorld/wall4.png'),
    "5": pygame.image.load('./Proyecto3-3DWorld/wall5.png'),
}

sprite1 = pygame.image.load('./Proyecto3-3DWorld/sprite1.png')
sprite2 = pygame.image.load('./Proyecto3-3DWorld/sprite2.png')
sprite3 = pygame.image.load('./Proyecto3-3DWorld/sprite3.png')
sprite4 = pygame.image.load('./Proyecto3-3DWorld/sprite4.png')

enemies = [
    {
        "x": 120,
        "y": 120,
        "sprite": sprite1
    },
    {
        "x": 300,
        "y": 300,
        "sprite": sprite2
    }
]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.scale = 10
        self.player = {
            "x": int(self.blocksize + self.blocksize / 2),
            "y": int(self.blocksize + self.blocksize / 2),
            "fov": int(pi/3),
            "a": int(pi/3)
        }
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]
        self.map = []
        self.clearZ()

    def clearZ(self):
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_map(self):
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.block(x, y, walls[self.map[j][i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def draw_sprite(self, sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"],
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"])**2 +
            (self.player["y"] - sprite["y"])**2
        ) ** 0.5

        sprite_size = int(((self.width/2)/d) * self.height/self.scale)

        sprite_x = int(
            (self.width/2) +
            (sprite_a - self.player["a"]) *
            (self.width/2) / self.player["fov"]
            + sprite_size/2)

        sprite_y = int(self.height/2 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * 128 / sprite_size)
                ty = int((y - sprite_y) * 128 / sprite_size)

                c = sprite["sprite"].get_at((tx, ty))

                if c != TRANSPARENT:
                    if(x > int(self.width/2) and x < self.width):
                        if self.zbuffer[x - int(self.width/2)] >= d:
                            self.zbuffer[x - int(self.width/2)] = d
                            self.point(x, y, c)

    def draw_stake(self, x, h, c, tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

    def cast_ray(self, a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]

        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * self.blocksize
                hity = y - j * self.blocksize

                if 1 < hitx < self.blocksize-1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)
                return d, self.map[j][i], tx

            self.point(x, y)

            d += 1

    def render(self):
        self.draw_map()
        self.draw_player()
        density = 100

        # minimap
        for i in range(0, density):
            a = self.player["a"] - self.player["fov"] / \
                2 + self.player["fov"]*i/density
            d, c, tx = self.cast_ray(a)

        # line
        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)

        # draw in 3d
        density = 100
        for i in range(0, int(self.width/2)):
            a = self.player["a"] - self.player["fov"] / \
                2 + self.player["fov"]*i/(self.width/2)
            d, c, tx = self.cast_ray(a)
            x = int(self.width/2) + i
            h = (self.height /
                 (d * cos(a - self.player["a"]))) * self.height/self.scale

            if self.zbuffer[i] >= d:
                self.draw_stake(x, h, c, tx)
                self.zbuffer[i] = d

        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], (255, 0, 0))

        for enemy in enemies:
            self.draw_sprite(enemy)


pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map("./Proyecto3-3DWorld/map.txt")

running = True
while running:
    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))
    r.clearZ()
    r.render()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                r.player["a"] -= pi/25
            if event.key == pygame.K_d:
                r.player["a"] += pi/25

            if event.key == pygame.K_RIGHT:
                r.player["x"] += 10
            if event.key == pygame.K_LEFT:
                r.player["x"] -= 10
            if event.key == pygame.K_UP:
                r.player["y"] -= 10
            if event.key == pygame.K_DOWN:
                r.player["y"] += 10
