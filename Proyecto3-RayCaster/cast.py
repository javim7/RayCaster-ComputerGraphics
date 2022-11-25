import pygame
from math import *
from pygame.locals import *
from pygame import mixer


mixer.init()
zombieGrowl = pygame.mixer.Sound("./Proyecto3-RayCaster/SFX/zombie.mp3")
footsteps = pygame.mixer.Sound("./Proyecto3-RayCaster/SFX/footsteps2.mp3")


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
    "1": pygame.image.load('./Proyecto3-RayCaster/Walls/wall1.png'),
    "2": pygame.image.load('./Proyecto3-RayCaster/Walls/wall2.png'),
    "3": pygame.image.load('./Proyecto3-RayCaster/Walls/wall3.png'),
    "4": pygame.image.load('./Proyecto3-RayCaster/Walls/wall4.png'),
    "5": pygame.image.load('./Proyecto3-RayCaster/Walls/wall5.png'),
    "6": pygame.image.load('./Proyecto3-RayCaster/Walls/wall6.png'),
}

zombie1 = pygame.image.load('./Proyecto3-RayCaster/Sprites/zombie1.png')
zombie2 = pygame.image.load('./Proyecto3-RayCaster/Sprites/zombie2.png')
zombie3 = pygame.image.load('./Proyecto3-RayCaster/Sprites/zombie3.png')
zombie4 = pygame.image.load('./Proyecto3-RayCaster/Sprites/zombie4.png')
zombie5 = pygame.image.load('./Proyecto3-RayCaster/Sprites/zombie5.png')

enemies = [
    {
        "x": 100,
        "y": 220,
        "alive": True,
        "canDie": False,
        "playSound": True,
        "sprite": zombie1
    },
    {
        "x": 250,
        "y": 370,
        "alive": True,
        "canDie": False,
        "playSound": True,
        "sprite": zombie2
    },
    {
        "x": 75,
        "y": 400,
        "alive": True,
        "canDie": False,
        "playSound": True,
        "sprite": zombie3
    },
    {
        "x": 440,
        "y": 430,
        "alive": True,
        "canDie": False,
        "playSound": True,
        "sprite": zombie4
    },
    {
        "x": 440,
        "y": 80,
        "alive": True,
        "canDie": False,
        "playSound": True,
        "sprite": zombie5
    }
]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.blocksize = 50
        self.wallsize = 128
        self.spritesize = 128
        self.i = 0
        self.j = 0
        self.scale = 10
        self.collision = True
        self.previousMove = None
        self.player = {
            "x": int(self.blocksize + self.blocksize / 2),
            "y": int(self.blocksize + self.blocksize / 2),
            "fov": int(pi/3),
            "a": int(pi/3)
        }
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]
        self.map = []
        self.clearZ()
        self.playSound = True

    def clearZ(self):
        self.zbuffer = [99999 for z in range(0, int(self.width/2))]

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i - x) * self.wallsize / self.blocksize)
                ty = int((j - y) * self.wallsize / self.blocksize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def check_out_bounds(self):
        for i in range(0, int(self.width)):
            a = self.player["a"] - self.player["fov"] / 2 + \
                self.player["fov"] * i / (self.width / 2)
            d, c, tx = self.cast_ray(a)
            if d <= 10:
                return True
        return False

    def draw_map(self):
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                self.i = int(x/self.blocksize)
                self.j = int(y/self.blocksize)
                if self.map[self.j][self.i] != ' ':
                    self.block(x, y, walls[self.map[self.j][self.i]])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])

    def play_sound(self, sprite):
        while sprite["playSound"]:
            pygame.mixer.Sound.play(zombieGrowl)
            sprite["playSound"] = False

    def draw_sprite(self, sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"],
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"])**2 +
            (self.player["y"] - sprite["y"])**2
        ) ** 0.5

        if d < 100:
            sprite["canDie"] = True
            self.play_sound(sprite)

        sprite_size = int(((self.width/2)/d) * self.height/self.scale)

        sprite_x = int(
            (self.width/2) +
            (sprite_a - self.player["a"]) *
            (self.width/2) / self.player["fov"]
            + sprite_size/2)

        sprite_y = int(self.height/2 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * self.wallsize / sprite_size)
                ty = int((y - sprite_y) * self.wallsize / sprite_size)

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
            ty = int((y - start_y) * self.wallsize / height)
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

                tx = int(maxhit * self.wallsize / self.blocksize)
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

        # dibujar punto rojo en minimapa
        for enemy in enemies:
            if enemy["alive"]:
                self.point(enemy["x"], enemy["y"], (255, 0, 0))

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

            try:
                self.collision = True
                h = (self.height /
                     (d * cos(a - self.player["a"]))) * self.height/self.scale
                if self.zbuffer[i] >= d:
                    self.draw_stake(x, h, c, tx)
                    self.zbuffer[i] = d
            except ZeroDivisionError:
                self.collision = False
                self.movimiento()

        # dibujar enemigos
        for enemy in enemies:
            if enemy["alive"]:
                self.draw_sprite(enemy)

    def movimiento(self, event=None):

        if event == None:
            event = self.previousMove

        if event.key == pygame.K_RIGHT:
            if self.collision:
                self.player["x"] += 10
                pygame.mixer.Sound.play(footsteps)
            else:
                self.player["x"] -= 10
        if event.key == pygame.K_LEFT:
            if self.collision:
                self.player["x"] -= 10
                pygame.mixer.Sound.play(footsteps)
            else:
                self.player["x"] += 10
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if self.collision:
                self.player["y"] -= 10
                pygame.mixer.Sound.play(footsteps)
            else:
                self.player["y"] += 10
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.collision:
                self.player["y"] += 10
                pygame.mixer.Sound.play(footsteps)
            else:
                self.player["y"] -= 10
