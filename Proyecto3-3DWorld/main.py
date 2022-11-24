
from cast import *
import pygame
from math import *
from pygame.locals import *
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map("./Proyecto3-3DWorld/map.txt")


mixer.init()
footsteps = pygame.mixer.Sound("./Proyecto3-3DWorld/SFX/footsteps2.mp3")
mixer.music.load('Proyecto3-3DWorld/SFX/mysterious-music.mp3')
mixer.music.play()


def render_fondo(imagen):
    for x in range(0, r.width):
        for y in range(0, r.height):
            r.point(x, y, imagen.get_at((x, y)))


imgBienvenida = pygame.image.load("Proyecto3-3DWorld/Backgrounds/clue.jpg")

bienvenida = True
while bienvenida:
    render_fondo(imgBienvenida)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                bienvenida = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold=True)

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

            a = r.player["a"]
            if event.key == pygame.K_RIGHT:
                r.player["x"] += 10
                pygame.mixer.Sound.play(footsteps)
            if event.key == pygame.K_LEFT:
                r.player["x"] -= 10
                pygame.mixer.Sound.play(footsteps)
            if event.key == pygame.K_UP:
                r.player["y"] -= 10
                pygame.mixer.Sound.play(footsteps)
            if event.key == pygame.K_DOWN:
                r.player["y"] += 10
                pygame.mixer.Sound.play(footsteps)
