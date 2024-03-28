# Example file showing a basic pygame "game loop"
import pygame
from player import *
import sprites

# pygame setup
pygame.init()
screen_width = 1280
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# megaman sprite sheet load image
sprite_sheet_image = pygame.image.load("sprites/player/megaman-sprite1.png").convert_alpha()
sprite_sheet = sprites.SpriteSheet(sprite_sheet_image)

# Initialize joysticks
pygame.joystick.init()
num_joysticks = pygame.joystick.get_count()
joysticks = []
for i in range(num_joysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Joystick {i}: {joystick.get_name()}")


player1 = Player(600,500, sprite_sheet, 6)

# move variables
moving_left = False
moving_right = False
jump_check = False 
gravity = 0.75          

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_SPACE:
                player1.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_SPACE:
                player1.jump = False
                
        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 14:
                moving_right = True
            if event.button == 13:
                moving_left = True
            if event.button == 1:
                player1.jump = True
                
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 14:
                moving_right = False
            if event.button == 13:
                moving_left = False
            if event.button == 1:
                player1.jump = False
                

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((159, 238, 252))
    pygame.draw.line(screen, "black", (0, 600), (screen_width, 600), 3)
    player1.get_input(moving_right, moving_left, gravity)
    player1.draw(screen)
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()