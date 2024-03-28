import pygame
import sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image1, image2, speed):
        super().__init__()
        self.jump = False
        self.in_air = True
        self.alive = True
        self.image2 = image2
        self.image1 = image1
        self.vel_x = speed
        self.vel_y = 0
        self.direction = 1
        self.flip = False
        self.flip_adj = False

        self.animation_list = []
        self.animation_steps1 = [3,4]
        self.animation_steps2 = [3]
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
        self.frame = 0
        self.step_counter = 0
        # animation list: 0:idle, 1:run, 2:jump, 3:idleshoot, 4:jumpshoot, 5:runshoot
        self.action = 0
        self.reverse_playback = False

        # grab animations for animation list
        for animation in self.animation_steps1:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.image1.get_image(self.step_counter, 24, 24, 4))
                self.step_counter += 1
            
            self.animation_list.append(temp_img_list)
        # this is the frame for jumping
        self.animation_list.append([self.image1.get_image(6.6, 26, 31, 4)])
        # this is for idle shoot
        self.animation_list.append([self.image2.get_image(2.935,31,24,4)])

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        print(self.animation_list)
        if self.action == 3 and self.flip == True:
            self.rect.x += 300
    def get_input(self, moving_right, moving_left, gravity, shoot):
        if self.alive:
            dx = 0
            dy = 0
            if shoot:
                self.action = 3
                print(self.action)
                print(self.frame)
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
            

            if self.jump == True and self.in_air == False:
                self.vel_y = -15
                self.action = 2
                self.jump = False
                self.in_air = True

            #update gravity
            self.vel_y += gravity
            if self.vel_y > 15:
                self.vel_y
            dy += self.vel_y

            # check collision with floor
            if self.rect.bottom + dy > 600:
                if shoot == False and moving_right == False and moving_left == False:
                    self.action = 0
                dy = 600 - self.rect.bottom
                self.in_air = False

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
            self.animation_cooldown = 150
        if self.in_air:
            self.action = 2


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
        # display.blit(self.animation_list[3][0],self.rect)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        super().__init__()
        self.speed = 15
        self.image = image.get_image(0,6,6,3)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        if self.direction == 1:
            self.rect.centerx += self.speed
        if self.direction == -1:
            self.rect.centerx -= self.speed