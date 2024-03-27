import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

# image function for frames

    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0,0), (frame*width,0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
