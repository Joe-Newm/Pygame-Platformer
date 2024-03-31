import pygame
import sprites

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

        self.animation_list = []
        self.animation_steps1 = [2,4,1]
        self.animation_steps2 = [3,1]
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
        self.frame = 0
        self.step_counter = 0
        # animation list: 0:idle, 1:run, 2:jump, 3:runshoot, 4:idleshoot, 5:jumpshoot
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
        
        #shoot up animation
        self.animation_list.append([self.image2.get_image((0,0), 4, 31,33,4)])
        self.animation_list.append([self.image2.get_image((0,0), 5, 31,34,4)])

        #pos = screen.get_rect().center
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        
        

        self.rect.midbottom = pos
    
        
    def get_input(self,look_up, moving_right, moving_left, gravity, shoot, bullet_group, bullet_image):
        if self.alive:
            dx = 0
            dy = 0

            if look_up and shoot:
                self.action = 6
                self.shoot(bullet_group, bullet_image, look_up, moving_right,moving_left)
            elif look_up:
                self.action = 6
            elif shoot:
                self.action = 4
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
                    self.action = 5
            # update position
            self.rect.x += dx
            self.rect.y += dy
                
            

    def shoot(self, bullet_group, bullet_image, look_up,moving_right, moving_left):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 13  
            if look_up and self.direction == 1 and not moving_right:
                bullet = Bullet(self.rect.centerx + 15, self.rect.centery -60, self.direction, bullet_image, True)
            elif look_up and self.direction == -1 and not moving_left:
                bullet = Bullet(self.rect.centerx -15, self.rect.centery -60, self.direction, bullet_image, True)

            elif self.direction == 1:
                bullet = Bullet(self.rect.right,self.rect.centery,self.direction, bullet_image, False)
            else:
                bullet = Bullet(self.rect.left,self.rect.centery,self.direction, bullet_image, False)
            
            bullet_group.add(bullet)

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
        
            
    def draw(self, display, gravity, shoot, moving_right, moving_left, look_up):
        self.animations()
        display.blit(pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False), self.rect)
        # display.blit(self.animation_list[3][0],self.rect)

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
        self.speed = 15
        self.image = image.get_image((0,0),0,10,10,3)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.direction = direction

        if look_up:
            self.up = True
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.up = False

    def update(self, player1, enemy1,bullet_group, screen):
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
        pygame.draw.rect(screen, "green", player1.rect, 1 )
        pygame.draw.rect(screen, "green", enemy1.rect, 1 )
        if pygame.sprite.spritecollide(player1,bullet_group, False):
            pygame.draw.rect(screen, "red", player1.rect, 1)
            if pygame.sprite.spritecollide(player1,bullet_group, False, pygame.sprite.collide_mask):
                if player1.alive:

                    player1.health -= 5
                    self.kill()

        if pygame.sprite.spritecollide(enemy1,bullet_group, False):
            if pygame.sprite.spritecollide(enemy1, bullet_group, False, pygame.sprite.collide_mask):
                pygame.draw.rect(screen, "red", enemy1.rect, 1 )
                if enemy1.alive:
                    enemy1.health -= 25
                    print(enemy1.health)
                    self.kill()