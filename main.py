# Example file showing a basic pygame "game loop"
import pygame
from pygame import mixer
from player import *
import sprites
from player import Bullet
from world import *

# pygame setup
pygame.init()
mixer.init()
mixer.music.load("sound/02-title.mp3")
mixer.music.set_volume(0.4)
mixer.music.play(-1)
screen_width = 1280
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True


# megaman sprite sheet load image
sprite_sheet_image1 = pygame.image.load("sprites/player/megaman-sprite1.png").convert_alpha()
sprite_sheet1 = sprites.SpriteSheet(sprite_sheet_image1)
sprite_sheet_image2 = pygame.image.load("sprites/player/megaman-sprite2.png").convert_alpha()
sprite_sheet2 = sprites.SpriteSheet(sprite_sheet_image2)

# enemy sprite sheet and load image
enemy_sheet_image1 = pygame.image.load("sprites/enemy/enemy-sprite1.png").convert_alpha()
enemy_sheet1 = sprites.SpriteSheet(enemy_sheet_image1)
enemy_sheet_image2 = pygame.image.load("sprites/enemy/enemy-sprite2.png").convert_alpha()
enemy_sheet2 = sprites.SpriteSheet(enemy_sheet_image2)

# grass map tile png
grass_sheet = pygame.image.load("sprites/map/grass.png").convert_alpha()
grass_object = sprites.SpriteSheet(grass_sheet)
grass_image = grass_object.get_image((0,0),0,30,30,4)

# world object and data
enemy_group = pygame.sprite.Group()
world = World()
player1, enemy_group = world.process_data(level_data, grass_image, sprite_sheet1, sprite_sheet2, enemy_sheet1, enemy_sheet2, enemy_group)

# bullet png
bullet_sheet = pygame.image.load("sprites/bullet/bullet.png").convert_alpha()
bullet_image = sprites.SpriteSheet(bullet_sheet)
bullet_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()

# Initialize joysticks
pygame.joystick.init()
num_joysticks = pygame.joystick.get_count()
joysticks = []
joystick_initialized = False
for i in range(num_joysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Joystick {i}: {joystick.get_name()}")

# player object


# move variables
look_up = False
moving_left = False
moving_right = False
jump_check = False 
shoot = False
gravity = 1





while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYDEVICEADDED and not joystick_initialized:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                joystick_initialized = True
                print("Joystick initialized:", joystick.get_name())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                look_up = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_SPACE:
                player1.jump = True
            if event.key == pygame.K_x:
                shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                look_up = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_SPACE:
                player1.jump = False
                jump_lock = True
            if event.key == pygame.K_x:
                shoot = False
                
        # xbox controller
        if event.type == pygame.JOYHATMOTION:
            #print("Button pressed:", event.value)
            if event.value == (1,0) or event.value == (1,1):
                moving_right = True
            else:
                moving_right = False
            if event.value == (-1,0) or event.value == (-1,1):
                moving_left = True
            else:
                moving_left = False
            if event.value == (0,1):
                look_up = True
            else:
                look_up = False

        if event.type == pygame.JOYBUTTONDOWN:
            #print("Button pressed:", event.button)
            if event.button == 14:
                moving_right = True
            if event.button == 13:
                moving_left = True
            if event.button == 1:
                player1.jump = True
            if event.button == 0:
                shoot = True
            if event.button == 11:
                look_up = True
            
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 14:
                moving_right = False
            if event.button == 13:
                moving_left = False
            if event.button == 1:
                player1.jump = False
            if event.button == 0:
                shoot = False
            if event.button == 11:
                look_up = False
                

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((112, 217, 255))
    
    screen_scroll = player1.get_input(look_up, moving_right, moving_left, gravity, shoot, player_bullet_group, bullet_image)

    #draw world
    world.draw(screen, screen_scroll, player1)

    player1.draw(screen, screen_scroll,player1)
    #add enemy to group
    for enemy in enemy_group:
        enemy.draw(screen, screen_scroll, player1)
        enemy.ai( gravity, moving_right, moving_left, shoot, player1, bullet_group, bullet_image)
    bullet_group.update(player1,enemy_group,player_bullet_group, bullet_group, screen)
    player_bullet_group.update(player1,enemy_group,player_bullet_group, bullet_group, screen)

    # shoot
    bullet_group.draw(screen)
    player_bullet_group.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()