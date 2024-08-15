import pygame
import math

def handle_movement(coords, angle, move, rotate, width, height, objects):
    mx = move * math.cos(angle)
    my = move * math.sin(angle)
    dx, dy = 0, 0

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        dx += mx
        dy += my
    if pressed[pygame.K_s]:
        dx -= mx
        dy -= my
    if pressed[pygame.K_a]:
        dx += my
        dy -= mx
    if pressed[pygame.K_d]:
        dx -= my
        dy += mx

    if (int(coords[0] + dx), int(coords[1])) not in objects:
        coords[0] += dx
    if (int(coords[0]), int(coords[1] + dy)) not in objects:
        coords[1] += dy

    # Handle mouse rotation
    if mouse_x < 100 or mouse_x > width - 100:
        pygame.mouse.set_pos([width // 2, height // 2])
    rel = pygame.mouse.get_rel()[0]
    rel = max(-40, min(40, rel))  # Limit the mouse movement to prevent extreme rotation
    angle += rel * rotate

    return angle
