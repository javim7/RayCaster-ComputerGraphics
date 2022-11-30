
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
r.load_map("./map.txt")
crosshair = pygame.image.load("./Sprites/crosshair.png")
gunPOV = pygame.image.load("./Sprites/gunPOV.png")

mixer.init()
shot = pygame.mixer.Sound("./SFX/shot.mp3")
mixer.music.load('./SFX/mysterious-music.mp3')
mixer.music.play(-1)

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


imgBienvenida = pygame.image.load("./Backgrounds/START.png")
imgControls = pygame.image.load("./Backgrounds/CONTROLS.png")
imgCompletado = pygame.image.load("./Backgrounds/FINISH.png")

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
    screen.blit(crosshair, (r.width - 300, r.height/2 - 60))
    screen.blit(gunPOV, (r.width - 350, r.height/2))
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

            r.previousMove = event
            r.movimiento(event)

    if muertos == 5:
        time.sleep(1)
        running = False
        completado = True

while completado:
    render_fondo(imgCompletado)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
