import pygame
import math

pygame.init()

width, height = 1200, 600

root = pygame.display.set_mode((width, height))

pygame.mouse.set_visible(False)

GRID = 100

gameover = False

clock = pygame.time.Clock()

# Load the map from a .txt file
def load_map(filename):
    global MAP, objects
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

load_map('map.txt')  # Load the map

coords = [1.5, 1.5]
angle = 0
fov = math.pi / 3
max_depth = 10
number_of_rays = width // 2
delta_angle = fov / number_of_rays

scale = width // number_of_rays

screen_distance = (width / 2) / math.tan(fov / 2)

move = 0.060
rotate = 0.050

colors = {1: (0, 255, 255)}  # Only one color now

# Load the texture image
texture_image = pygame.image.load('textures.png')
texture_size = 64  # Size of each texture in the image

def setup_map():
    pygame.draw.rect(root, (50, 50, 50), (0, height // 2, width, height))
    pygame.draw.rect(root, (30, 30, 30), (0, 0, width, height // 2))

def movements():
    global angle
    mx = move * math.cos(angle)
    my = move * math.sin(angle)
    dx, dy = 0, 0

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        dx += mx
        dy += my
    if pressed[pygame.K_s]:
        dx += -mx
        dy += -my
    if pressed[pygame.K_a]:
        dx += my
        dy += -mx
    if pressed[pygame.K_d]:
        dx += -my
        dy += mx

    if (int(coords[0] + dx), int(coords[1])) not in objects:
        coords[0] += dx
    if (int(coords[0]), int(coords[1] + dy)) not in objects:
        coords[1] += dy

    if mouse_x < 100 or mouse_x > width - 100:
        pygame.mouse.set_pos([width // 2, height // 2])
    rel = pygame.mouse.get_rel()[0]
    rel = max(-40, min(40, rel))
    angle += rel * 0.002

def raycast():
    global objects  # Add this line to access the global objects variable
    ray_angle = (angle - (fov / 2)) + 0.000001
    color = 0

    for ray in range(number_of_rays):

        sin_angle = math.sin(ray_angle)
        cos_angle = math.cos(ray_angle)

        # Vertical
        x_vertical, dx = (int(coords[0]) + 1, 1) if cos_angle > 0 else (int(coords[0]) - 0.000001, -1)
        depth_vertical = (x_vertical - coords[0]) / cos_angle

        y_vertical = (depth_vertical * sin_angle) + coords[1]

        delta_depth = dx / cos_angle
        dy = delta_depth * sin_angle

        for i in range(max_depth):
            tile_vertical = (int(x_vertical), int(y_vertical))
            if tile_vertical in objects:
                break
            x_vertical += dx
            y_vertical += dy
            depth_vertical += delta_depth

        # Horizontal
        y_horizontal, dy = (int(coords[1]) + 1, 1) if sin_angle > 0 else (int(coords[1]) - 0.000001, -1)
        depth_horizontal = (y_horizontal - coords[1]) / sin_angle

        x_horizontal = (depth_horizontal * cos_angle) + coords[0]

        delta_depth = dy / sin_angle
        dx = delta_depth * cos_angle

        for i in range(max_depth):
            tile_horizontal = (int(x_horizontal), int(y_horizontal))
            if tile_horizontal in objects:
                break
            x_horizontal += dx
            y_horizontal += dy
            depth_horizontal += delta_depth

        if depth_horizontal < depth_vertical:
            depth = depth_horizontal
            color = objects[tile_horizontal]
            texture_x = x_horizontal % 1
            side = 0
        elif depth_vertical < depth_horizontal:
            depth = depth_vertical
            color = objects[tile_vertical]
            texture_x = y_vertical % 1
            side = 1

        # Remove fish-eye effect
        depth = depth * (math.cos(angle - ray_angle))

        # Projection
        projection_height = screen_distance / (depth + 0.000001)

        # Get the correct texture column
        texture_column = int(texture_x * texture_size)
        if side == 1:
            texture_column = texture_size - texture_column - 1

        # Ensure the texture column is within valid bounds
        texture_column = max(0, min(texture_column, texture_size - 1))

        # Draw the textured wall
        texture_rect = pygame.Rect(texture_column, 0, 1, texture_size)

        # Ensure the texture_rect is within the surface area
        if texture_rect.right <= texture_image.get_width() and texture_rect.bottom <= texture_image.get_height():
            texture_slice = pygame.transform.scale(texture_image.subsurface(texture_rect), (scale, projection_height))
            root.blit(texture_slice, (ray * scale, (height // 2) - projection_height // 2))

        ray_angle += delta_angle


while not gameover:
    root.fill('black')

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            gameover = True
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_q:
                gameover = True

    setup_map()
    raycast()
    movements()

    pygame.display.set_caption(str(clock.get_fps() // 1))

    clock.tick(60)
    pygame.display.update()
