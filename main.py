import pygame
import math
from map_loader import load_map, setup_map
from movement import handle_movement
from raycasting import raycast
from textures import load_textures

pygame.init()

width, height = 1200, 600
root = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)

GRID = 100
gameover = False
clock = pygame.time.Clock()

# Load the map and textures
MAP, objects = load_map('map.txt')
textures = load_textures()

coords = [1.5, 1.5]
angle = 0
fov = math.pi / 3
max_depth = 10
number_of_rays = width // 2
delta_angle = fov / number_of_rays

scale = width // number_of_rays
screen_distance = (width / 2) / math.tan(fov / 2)

move = 0.060
rotate = 0.002

# Game loop
while not gameover:
    root.fill('black')

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            gameover = True
        if i.type == pygame.KEYUP and i.key == pygame.K_q:
            gameover = True

    setup_map(root, width, height)
    raycast(root, width, height, coords, angle, fov, number_of_rays, delta_angle, max_depth, screen_distance, scale,
            objects, textures)

    angle = handle_movement(coords, angle, move, rotate, width, height, objects)

    pygame.display.set_caption(str(clock.get_fps() // 1))

    clock.tick(60)
    pygame.display.update()
