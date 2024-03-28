import pygame
import sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.jump = False
        self.alive = True
        self.image = image
        frame = self.image.get_image(0,24,24,3)
        self.rect = frame.get_rect()
        self.rect.center = (x, y)
        self.vel_x = speed
        self.vel_y = 0
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
        # this is the frame for jumping
        self.animation_list.append([self.image.get_image(5.8, 26, 31, 4)])

    def get_input(self, moving_right, moving_left, gravity):
        if self.alive:
            dx = 0
            dy = 0

            if moving_right:
                dx = self.vel_x
                self.flip = False
                self.direction = 1
                self.action = 1
            elif moving_left:
                dx = -self.vel_x
                self.flip = True
                self.direction = -1
                self.action = 1
            else:
                self.action = 0

            if self.jump == True:
                self.vel_y = -15
                self.action = 2
                self.jump = False

            #update gravity
            self.vel_y += gravity
            if self.vel_y > 15:
                self.vel_y
            dy += self.vel_y

            # check collision with floor
            if self.rect.bottom + dy > 578:
                dy = 578 - self.rect.bottom
            else:
                self.action = 2

            # update position
            self.rect.x += dx
            self.rect.y += dy

    def animations(self):
        #chooses cooldown for each animation
        if self.action == 0:
            self.animation_cooldown = 2000
        if self.action == 0 and self.frame == 1:
            self.animation_cooldown = 150
        if self.action == 1:
            self.animation_cooldown = 125

        # animates based on which animation is in animation_list
        
        current_time = pygame.time.get_ticks()
        time_since_last_update = current_time - self.last_update
        frames_to_skip = time_since_last_update // self.animation_cooldown

        # Update frame based on elapsed time and cooldown
        self.frame += frames_to_skip
        self.last_update += frames_to_skip * self.animation_cooldown

        # Ensure frame is within bounds for the current action
        if self.action == 0:
            if self.frame == 2:
                self.frame = 0
        if self.frame >= len(self.animation_list[self.action]):
            self.frame = 0
        
            

    def draw(self, display):
        self.animations()
        display.blit(pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False), self.rect)