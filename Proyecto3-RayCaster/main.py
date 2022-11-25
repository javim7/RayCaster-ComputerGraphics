
from cast import *
import pygame
from math import *
from pygame.locals import *
from pygame import mixer
import time

pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
r = Raycaster(screen)
r.load_map("./Proyecto3-RayCaster/map.txt")


mixer.init()
footsteps = pygame.mixer.Sound("./Proyecto3-RayCaster/SFX/footsteps2.mp3")
shot = pygame.mixer.Sound("./Proyecto3-RayCaster/SFX/shot.mp3")
mixer.music.load('Proyecto3-RayCaster/SFX/mysterious-music.mp3')
mixer.music.play()

muertos = 0


def update_fps():
    fps = str(round(float(clock.get_fps()), 3))
    fps_text = font.render("FPS = " + fps, 1, pygame.Color("White"))
    return fps_text


def update_enemies():
    global muertos
    enemies_text = font.render(
        "Killed = " + str(muertos) + "/5", 1, pygame.Color("White"))
    return enemies_text


def kill_enemy():
    global muertos
    pygame.mixer.Sound.play(shot)
    for enemy in enemies:
        if enemy["canDie"] and enemy["alive"]:
            enemy["alive"] = False
            muertos += 1


def render_fondo(imagen):
    for x in range(0, r.width):
        for y in range(0, r.height):
            r.point(x, y, imagen.get_at((x, y)))


imgBienvenida = pygame.image.load("Proyecto3-RayCaster/Backgrounds/START.png")
imgControls = pygame.image.load("Proyecto3-RayCaster/Backgrounds/CONTROLS.png")
imgCompletado = pygame.image.load("Proyecto3-RayCaster/Backgrounds/FINISH.png")

bienvenida = True
controls = False
completado = False
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
                bienvenida = False
                controls = True

while controls:
    render_fondo(imgControls)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                controls = False

running = True
while running:
    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(GROUND, (r.width/2, r.height/2, r.width, r.height/2))

    r.clearZ()
    r.render()

    screen.blit(update_fps(), (r.width - 85, r.height - 480))
    screen.blit(update_enemies(), ((r.width / 2) + 10, r.height - 480))
    clock.tick(60)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                kill_enemy()

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
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                r.player["y"] -= 10
                pygame.mixer.Sound.play(footsteps)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                r.player["y"] += 10
                pygame.mixer.Sound.play(footsteps)

    if muertos == 2:
        time.sleep(1)
        running = False
        completado = True

while completado:
    render_fondo(imgCompletado)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
