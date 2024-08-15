# raycasting.py
import pygame
import math

def raycast(root, width, height, coords, angle, fov, number_of_rays, delta_angle, max_depth, screen_distance, scale, objects, textures):
    ray_angle = (angle - (fov / 2)) + 0.000001

    # Initialize depth buffer
    depth_buffer = [float('inf')] * number_of_rays

    for ray in range(number_of_rays):
        sin_angle = math.sin(ray_angle)
        cos_angle = math.cos(ray_angle)

        # Vertical checking
        x_vertical, dx = (int(coords[0]) + 1, 1) if cos_angle > 0 else (int(coords[0]) - 0.000001, -1)
        depth_vertical = (x_vertical - coords[0]) / cos_angle
        y_vertical = (depth_vertical * sin_angle) + coords[1]

        delta_depth = dx / cos_angle
        dy = delta_depth * sin_angle

        for i in range(max_depth):
            tile_vertical = (int(x_vertical), int(y_vertical))
            if tile_vertical in objects:
                wall_type = objects[tile_vertical]
                break
            x_vertical += dx
            y_vertical += dy
            depth_vertical += delta_depth

        # Horizontal checking
        y_horizontal, dy = (int(coords[1]) + 1, 1) if sin_angle > 0 else (int(coords[1]) - 0.000001, -1)
        depth_horizontal = (y_horizontal - coords[1]) / sin_angle
        x_horizontal = (depth_horizontal * cos_angle) + coords[0]

        delta_depth = dy / sin_angle
        dx = delta_depth * cos_angle

        for i in range(max_depth):
            tile_horizontal = (int(x_horizontal), int(y_horizontal))
            if tile_horizontal in objects:
                wall_type = objects[tile_horizontal]
                break
            x_horizontal += dx
            y_horizontal += dy
            depth_horizontal += delta_depth

        if depth_horizontal < depth_vertical:
            depth = depth_horizontal
            texture_x = x_horizontal % 1
            side = 0
        else:
            depth = depth_vertical
            texture_x = y_vertical % 1
            side = 1

        # Remove fish-eye effect
        depth = depth * (math.cos(angle - ray_angle))

        # Update depth buffer and only draw if this ray hits the closest wall
        if depth < depth_buffer[ray]:
            depth_buffer[ray] = depth
            projection_height = screen_distance / (depth + 0.000001)

            # Get the correct texture column
            texture_column = int(texture_x * textures[wall_type].get_width())
            if side == 1:
                texture_column = textures[wall_type].get_width() - texture_column - 1

            # Ensure the texture column is within valid bounds
            texture_column = max(0, min(texture_column, textures[wall_type].get_width() - 1))

            # Draw the textured wall
            texture_rect = pygame.Rect(texture_column, 0, 1, textures[wall_type].get_height())
            texture_slice = pygame.transform.scale(textures[wall_type].subsurface(texture_rect), (scale, projection_height))
            root.blit(texture_slice, (ray * scale, (height // 2) - projection_height // 2))

        ray_angle += delta_angle
