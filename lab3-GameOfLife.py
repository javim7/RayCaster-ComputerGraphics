import pygame
from random import randint
from copy import deepcopy

resolucion = width, height = 1200, 750
Tile = 10

w, h = width // Tile, height // Tile

FPS = 10

pygame.init()
surface = pygame.display.set_mode(resolucion)
clock = pygame.time.Clock()

# estado actual y siguiente estado
next_field = [[0 for i in range(w)]for j in range(h)]
'''
Patrones iniciales
'''
# ----patron inicial random
# current_field = [[randint(0, 1) for i in range(w)] for j in range(h)]
# ----patron experimentado con el modulo de 25
current_field = [[1 if not (i*j) % 25 else 0 for i in range(w)]
                 for j in range(h)]


# funcion para poder ver el estado de cada celula


def check_cell(current_field, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


while True:

    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # dibujando el grid
    [pygame.draw.line(surface, pygame.Color('black'), (x, 0), (x, height))
     for x in range(0, width, Tile)]
    [pygame.draw.line(surface, pygame.Color('black'), (0, y), (width, y))
     for y in range(0, height, Tile)]

    # dibujar la vida
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if current_field[y][x]:
                pygame.draw.rect(surface, pygame.Color(
                    'red'), (x * Tile + 2, y * Tile + 2, Tile - 2, Tile - 2))
                # pygame.Surface.set_at(
                #     surface, (x * Tile + 2, y * Tile + 2), pygame.Color('red'))
            next_field[y][x] = check_cell(current_field, x, y)

    current_field = deepcopy(next_field)

    pygame.display.flip()
    clock.tick(FPS)
