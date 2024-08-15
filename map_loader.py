import pygame

MAP = []
objects = {}

def load_map(filename):
    MAP = []
    objects = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for y, line in enumerate(lines):
            row = [int(char) for char in line.strip()]
            MAP.append(row)
            for x, value in enumerate(row):
                if value:
                    objects[(x, y)] = value
    return MAP, objects  # Return the map and objects

def setup_map(root, width, height):
    pygame.draw.rect(root, (50, 50, 50), (0, height // 2, width, height))
    pygame.draw.rect(root, (30, 30, 30), (0, 0, width, height // 2))
