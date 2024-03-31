import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

# image function for frames

    def get_image(self,y, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, y, (frame*width,0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
    
    def getMaskRect(self,surf, top = 0, left = 0):
        surf_mask = pygame.mask.from_surface(surf)
        rect_list = surf_mask.get_bounding_rects()
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect

