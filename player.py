import pygame
import sprites
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image1, image2, speed):
        super().__init__()
        self.health = 100
        self.max_health = self.health
        self.jump = False
        self.in_air = True
        self.alive = True
        self.image2 = image2
        self.image1 = image1
        self.vel_x = speed
        self.vel_y = 0
        self.shoot_cooldown = 0
        self.direction = 1
        self.flip = False
        self.flip_adj = False
        self.pos = pos
        
        # ai variables
        self.vision = pygame.Rect(0,0,800,20)
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0

        #sprite animation variables
        self.animation_list = []
        self.animation_steps1 = [2,4,1]
        self.animation_steps2 = [3]
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
        self.frame = 0
        self.step_counter = 0
        # animation list: 0:idle, 1:run, 2:jump, 3:runshoot, 4:jumpshoot, 5:shootup, 6:idleshoot, 7:death
        self.action = 0
        self.reverse_playback = False

        # grab animations for animation list
        for animation in self.animation_steps1:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.image1.get_image((0,0),self.step_counter, 31, 35, 4))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)
        self.step_counter = 0
        for animation in self.animation_steps2:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.image2.get_image((0,0),self.step_counter, 31, 35, 4))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)
        
        #jump shoot animation
        self.animation_list.append([self.image2.get_image((0,0), 3, 31,33,4)])
        #shoot up animation
        self.animation_list.append([self.image2.get_image((0,0), 4, 31,34,4)])
        #idle shoot animation
        self.animation_list.append([self.image2.get_image((0,0), 4.5, 35,34,4)])
        #death animation
        self.animation_list.append([self.image2.get_image((0,0), 6.2, 31,34,4)])

        #object rect
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
    
        
    def get_input(self,look_up, moving_right, moving_left, gravity, shoot, bullet_group, bullet_image):
        if self.alive:
            dx = 0
            dy = 0

            if look_up and shoot:
                self.action = 5
                self.shoot(bullet_group, bullet_image, look_up, moving_right,moving_left)
            elif look_up:
                self.action = 5
            elif shoot:
                self.action = 6
                self.shoot(bullet_group, bullet_image, look_up,moving_right,moving_left)
            if moving_right:
                dx = self.vel_x
                self.flip = False
                self.direction = 1
                self.action = 1
                if shoot == True:
                    self.action = 3
            elif moving_left:
                dx = -self.vel_x
                self.flip = True
                self.direction = -1
                self.action = 1
                if shoot == True:
                    self.action = 3
            

            if self.jump == True and self.in_air == False:
                self.vel_y = -15
                self.action = 2
                self.jump = False
                self.in_air = True
            if self.in_air:
                self.action = 2
                if shoot:
                    self.action = 4
            # update position
            self.rect.x += dx
            self.rect.y += dy
                
            

    def shoot(self, player_bullet_group, bullet_image, look_up,moving_right, moving_left):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 13  
            if look_up and self.direction == 1 and not moving_right:
                bullet = Bullet(self.rect.centerx + 15, self.rect.centery -70, self.direction, bullet_image, True)
            elif look_up and self.direction == -1 and not moving_left:
                bullet = Bullet(self.rect.centerx -15, self.rect.centery -70, self.direction, bullet_image, True)

            elif self.direction == 1:
                bullet = Bullet(self.rect.right +25,self.rect.centery,self.direction, bullet_image, False)
            else:
                bullet = Bullet(self.rect.left - 10,self.rect.centery,self.direction, bullet_image, False)
            
            player_bullet_group.add(bullet)

    def animations(self):
        #chooses cooldown for each animation
        if self.action == 0:
            self.animation_cooldown = 2000
        if self.action == 0 and self.frame == 1:
            self.animation_cooldown = 150
        if self.action == 1:
            self.animation_cooldown = 150
        if self.action == 3:
            self.animation_cooldown = 150
        if self.action == 4:
            self.animation_cooldown = 200
        # bullet cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


        # animates based on which animation is in animation_list
        
        current_time = pygame.time.get_ticks()
        time_since_last_update = current_time - self.last_update
        frames_to_skip = time_since_last_update // self.animation_cooldown

        # Update frame based on elapsed time and cooldown
        self.frame += frames_to_skip
        self.last_update += frames_to_skip * self.animation_cooldown

        # Ensure frame is within bounds for the current action
        
        if self.frame >= len(self.animation_list[self.action]):
            self.frame = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()
            self.action = 7

    def ai(self, screen, shoot, player1, bullet_group, bullet_image):
        look_up= 0
        gravity = 0
        shoot = 0
        ai_moving_left = False
        ai_moving_right = False
        if self.alive and player1.alive:
            if self.idling == False and random.randint(1,200) == 1:
                self.idling = True
                self.idling_counter = 100
                self.action = 0
            if pygame.Rect.colliderect(self.vision, player1.rect):
                self.shoot(bullet_group, bullet_image, look_up, ai_moving_right, ai_moving_left)
                self.action = 6
                self.idling = True
            if self.idling == False:
                self.action = 1
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.get_input(look_up, ai_moving_right, ai_moving_left, gravity, shoot, bullet_group, bullet_image)
                self.move_counter += 1
                # vision for ai
                self.vision.center = (self.rect.centerx + 400 * self.direction, self.rect.centery)
                #pygame.draw.rect(screen, "red", self.vision)
                

                if self.move_counter > 50:
                    self.direction *= -1
                    self.move_counter = 0
            else: 
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
            
    def draw(self, display, gravity, shoot, moving_right, moving_left, look_up):
        self.animations()
        display.blit(pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False), self.rect)

        #update gravity
        dx = 0
        dy = 0
        self.vel_y += gravity
        if self.vel_y > 15:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 620:
            if shoot == False and moving_right == False and moving_left == False and look_up == False:
                self.action = 0
            dy = 620 - self.rect.bottom
            self.in_air = False

        # update position
        self.rect.x += dx
        self.rect.y += dy

        #check alive
        self.check_alive()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, look_up):
        super().__init__()
        self.speed = 17
        self.image = image.get_image((0,0),0,10,10,3)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.direction = direction

        if look_up:
            self.up = True
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.up = False

    def update(self, player1, enemy1,player_bullet_group, bullet_group, screen):
        if self.up:
            self.rect.centery -= self.speed
        else:
            self.rect.centerx += (self.direction)*self.speed
        #check if bullets have left screen
        if self.rect.right < 0 or self.rect.left > 1280:
            self.kill()
        if self.rect.bottom < 0 or self.rect.top > 1280:
            self.kill()
        

        #check collision with characters
        if pygame.sprite.spritecollide(player1,bullet_group, False):
            #pygame.draw.rect(screen, "red", player1.rect, 1)
            if pygame.sprite.spritecollide(player1,bullet_group, True, pygame.sprite.collide_mask):
                if player1.alive:
                    player1.health -= 5
                    print(player1.health)
                    

                    flashing_surface = player1.animation_list[player1.action][player1.frame].copy()
                    new_rect = flashing_surface.get_rect()
                    player1.mask = pygame.mask.from_surface(enemy1.animation_list[player1.action][player1.frame])
                    for x in range(new_rect.width):
                        for y in range(new_rect.height):
                            # Check if the pixel is non-transparent in the mask
                            if player1.mask.get_at((x, y)):
                                # Fills corresponding pixel with white
                                flashing_surface.set_at((x, y), (255, 255, 255))

                    # Blit the the white surface on character to flash
                    screen.blit(pygame.transform.flip(flashing_surface, player1.flip, False), player1.rect)
                    
                    
                    
                    

        if pygame.sprite.spritecollide(enemy1,player_bullet_group, False):
            if pygame.sprite.spritecollide(enemy1, player_bullet_group, False, pygame.sprite.collide_mask):
                # Iterate over each pixel of the image for flash effect
                if enemy1.alive:
                    enemy1.health -= 15
                    print(enemy1.health)
                    self.kill()
                    flashing_surface = enemy1.animation_list[enemy1.action][enemy1.frame].copy()
                    new_rect = enemy1.animation_list[enemy1.action][enemy1.frame].get_rect()
                    enemy1.mask = pygame.mask.from_surface(enemy1.animation_list[enemy1.action][enemy1.frame])
                    for x in range(new_rect.width):
                        for y in range(new_rect.height):
                            # Check if the pixel is non-transparent in the mask
                            if enemy1.mask.get_at((x, y)):
                                # Fills corresponding pixel with white
                                flashing_surface.set_at((x, y), (255, 255, 255))

                    # Blit the the white surface on character to flash
                    screen.blit(pygame.transform.flip(flashing_surface, enemy1.flip, False), enemy1.rect)
