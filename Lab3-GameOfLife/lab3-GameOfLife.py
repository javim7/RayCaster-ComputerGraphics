# importando librerias externas
import pygame
from random import randint
from copy import deepcopy

resolucion = width, height = 1200, 750
Tile = 10

w, h = width // Tile, height // Tile

FPS = 10

pygame.init()
superficie = pygame.display.set_mode(resolucion)

# estado actual y siguiente estado
siguiente_estado = [[0 for i in range(w)]for j in range(h)]
'''
Patrones iniciales
'''
# ----patron inicial random
# estado_actual = [[randint(0, 1) for i in range(w)] for j in range(h)]
# ----patron experimentado con el modulo de 25
estado_actual = [[1 if not (i*j) % 25 else 0 for i in range(w)]
                 for j in range(h)]


# funcion para poder ver el estado de cada celula
def verificar_celula(estado_actual, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if estado_actual[j][i]:
                count += 1

    if estado_actual[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


while True:

    superficie.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # dibujando el grid
    [pygame.draw.line(superficie, pygame.Color('black'), (x, 0), (x, height))
     for x in range(0, width, Tile)]
    [pygame.draw.line(superficie, pygame.Color('black'), (0, y), (width, y))
     for y in range(0, height, Tile)]

    # dibujar la vida
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if estado_actual[y][x]:
                pygame.draw.rect(superficie, pygame.Color(
                    'red'), (x * Tile + 2, y * Tile + 2, Tile - 2, Tile - 2))
                # pygame.superficie.set_at(
                #     superficie, (x * Tile + 2, y * Tile + 2), pygame.Color('red'))
            siguiente_estado[y][x] = verificar_celula(estado_actual, x, y)

    estado_actual = deepcopy(siguiente_estado)

    pygame.display.flip()
