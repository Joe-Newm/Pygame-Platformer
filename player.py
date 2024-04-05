import pygame
import sprites
import random

class Player(pygame.sprite.Sprite):
    def __init__(self,char_type, pos, image1, image2, speed):
        super().__init__()
        self.char_type = char_type
        self.health = 10000
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
        self.jump_lock = False

        # ai variables
        self.vision = pygame.Rect(0,0,800,20)
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.ai_vel_y = 0

        #scroll variables
        self.scroll_thresh = 200
        self.screen_scroll = 0
        self.bg_scroll = 0

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
        #jump shoot up animation
        self.animation_list.append([self.image2.get_image((0,0), 7.2, 31, 34,4)])

        #object rect
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
    
        
    def get_input(self,look_up, moving_right, moving_left, gravity, shoot, bullet_group, bullet_image):
        screen_width = 1280
        screen_height = int(screen_width * 0.8)
        screen_scroll = 0
        if self.alive:
            dx = 0
            dy = 0
            
            if look_up and shoot:
                self.action = 5
                self.shoot(bullet_group, bullet_image, look_up, moving_right,moving_left)
            elif self.in_air and shoot and moving_left:
                self.action = 4
                self.shoot(bullet_group, bullet_image, look_up,moving_right,moving_left)

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
            elif shoot == False and look_up == False:
                self.action = 0
                
            
            if self.jump == True and self.jump_lock == False:
                self.action = 2
                self.vel_y -= 3
                self.in_air = True
                if self.vel_y < -18:
                    self.vel_y += gravity
                    self.jump = False
            else:
                self.jump = False
                if self.in_air == True and self.jump == False:
                    self.jump_lock = True
            print(self.jump)
            print(f"jumplock{self.jump_lock}")
                    
                

            if self.in_air:
                if shoot and moving_left:
                    self.action = 4
                elif shoot and moving_right:
                    self.action = 4
                elif look_up and shoot:
                    self.action = 8
                elif shoot:
                    self.action = 4
                else:
                    self.action = 2
            if self.in_air and self.jump == False:
                self.vel_y += gravity
            
 
            #update gravity   
            # if self.vel_y > 15:
            #     self.vel_y = 0
            print(self.vel_y)
            
            # check collision with floor
            if self.rect.bottom + dy > 620:
                self.vel_y = 0
                dy = 620 - self.rect.bottom
                self.in_air = False
                self.jump_lock = False
                
            dy += self.vel_y
            # update position
            self.rect.x += dx
            self.rect.y += dy

            # update scroll based on player position
            if self.char_type == "player":
                if self.alive == False:
                    screen_scroll = 0
                elif self.rect.right > screen_width - self.scroll_thresh or self.rect.left < self.scroll_thresh:
                    self.rect.x -= dx
                    screen_scroll = -dx   
            return screen_scroll
            

    def shoot(self, player_bullet_group, bullet_image, look_up,moving_right, moving_left):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 13  
            if look_up and self.direction == 1 and not moving_right:
                bullet = Bullet(self.rect.centerx + 14, self.rect.centery -60, self.direction, bullet_image, True)
            elif look_up and self.direction == -1 and not moving_left:
                bullet = Bullet(self.rect.centerx -14, self.rect.centery -60, self.direction, bullet_image, True)
            elif self.direction == 1:
                bullet = Bullet(self.rect.right +15,self.rect.centery -2,self.direction, bullet_image, False)
            else:
                bullet = Bullet(self.rect.left,self.rect.centery -2,self.direction, bullet_image, False)
            
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

    def ai(self, gravity, moving_right, moving_left, shoot, player1, bullet_group, bullet_image):
        dx = 0
        dy = 0
        look_up= 0
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
                if ai_moving_right:
                    dx = self.vel_x
                    self.flip = False
                    self.direction = 1
                    self.action = 1
                    if shoot == True:
                        self.action = 3
                elif ai_moving_left:
                    dx = -self.vel_x
                    self.flip = True
                    self.direction = -1
                    self.action = 1
                    if shoot == True:
                        self.action = 3
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
            #update gravity
            
            self.ai_vel_y += gravity
            if self.vel_y > 15:
                self.vel_y = 15
            dy += self.ai_vel_y
            # check collision with floor
            if self.rect.bottom + dy > 620:
                if shoot == False and moving_right == False and moving_left == False and look_up == False:
                    self.action = 0
                dy = 620 - self.rect.bottom
                self.in_air = False
            #update position
            self.rect.x += dx
            self.rect.y += dy
            
    def draw(self, display, screen_scroll, player1):
        self.animations()
        display.blit(pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False), self.rect)

        #check alive
        self.check_alive()
        if self.char_type == "enemy" and player1.alive:
            self.rect.x += screen_scroll
        

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

    def update(self, player1, enemy_group,player_bullet_group, bullet_group, screen):
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
        collided_bullets = pygame.sprite.spritecollide(player1,bullet_group, False)
        if collided_bullets:
            if pygame.sprite.spritecollide(player1,bullet_group, True, pygame.sprite.collide_mask):
                if player1.alive:
                    player1.health -= 5
                    try:
                        player_flashing_surface = player1.animation_list[player1.action][player1.frame].copy()
                    except IndexError:
                        print("Error: Animation index out of range for the player")
                        # Handle the error
                        player_flashing_surface = player1.animation_list[0][0].copy()
                    new_rect = player_flashing_surface.get_rect()
                    player1.mask = pygame.mask.from_surface(player_flashing_surface)
                    for x in range(new_rect.width):
                        for y in range(new_rect.height):
                            # Check if the pixel is non-transparent in the mask
                            if player1.mask.get_at((x, y)):
                                # Fills corresponding pixel with white
                                player_flashing_surface.set_at((x, y), (255, 255, 255))

                    # Blit the the white surface on character to flash
                    screen.blit(pygame.transform.flip(player_flashing_surface, player1.flip, False), player1.rect)
                    

        collided_player_bullets = pygame.sprite.groupcollide(enemy_group,player_bullet_group, False, False)
        if collided_player_bullets:
            collision = pygame.sprite.groupcollide(enemy_group, player_bullet_group, False, pygame.sprite.collide_mask)
            if collision:
                for enemy, bullet in collision.items():
                        
                        # Iterate over each pixel of the image for flash effect
                        if enemy.alive:
                            self.kill()
                            enemy.health -= 15
                            try:
                                flashing_surface = enemy.animation_list[enemy.action][enemy.frame].copy()
                            except IndexError:
                                print("Error: Animation index out of range")
                                # Handle the error
                                continue  # Skip 
                            new_rect = flashing_surface.get_rect()
                            enemy.mask = pygame.mask.from_surface(flashing_surface)
                            for x in range(new_rect.width):
                                for y in range(new_rect.height):
                                    # Check if the pixel is non-transparent in the mask
                                    if enemy.mask.get_at((x, y)):
                                        # Fills corresponding pixel with white
                                        flashing_surface.set_at((x, y), (255, 255, 255))

                            # Blit the the white surface on character to flash
                            screen.blit(pygame.transform.flip(flashing_surface, enemy.flip, False), enemy.rect)
