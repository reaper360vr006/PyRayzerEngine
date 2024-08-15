import pygame

def load_textures():
    # Load texture images
    texture_images = {
        1: pygame.image.load('textures/texture_1.png'),
        2: pygame.image.load('textures/texture_2.png'),
        # 3: pygame.image.load('texture3.png'),
        # Add more textures as needed
    }
    return texture_images