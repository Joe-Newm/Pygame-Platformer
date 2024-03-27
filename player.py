import pygame
import sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        
        self.image = image
        frame = self.image.get_image(0,24,24,3)
        self.rect = frame.get_rect()
        self.rect.center = (x, y)
        self.vel = speed
        self.direction = 1
        self.flip = False

        self.animation_list = []
        self.animation_steps = [3,3]
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
        self.frame = 0
        self.step_counter = 0
        self.action = 0

        # grab animations for animation list
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.image.get_image(self.step_counter, 24, 24, 4))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)

    def get_input(self, moving_right, moving_left):
        if moving_right:
            self.rect.x += self.vel
            self.flip = False
            self.direction = 1
            self.action = 1
        elif moving_left:
            self.rect.x -= self.vel
            self.flip = True
            self.direction = -1
            self.action = 1
        else:
            self.action = 0

        
            

    def draw(self, display):
        #chooses cooldown for each animation
        if self.action == 0:
            self.animation_cooldown = 2000
        if self.action == 0 and self.frame == 1:
            self.animation_cooldown = 150
        if self.action == 1:
            self.animation_cooldown = 150

        # animates based on which animation is in animation_list
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
        display.blit(pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False), self.rect)