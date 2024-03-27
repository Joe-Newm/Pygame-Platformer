# Example file showing a basic pygame "game loop"
import pygame
from player import *
import sprites

# pygame setup
pygame.init()
screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# megaman sprite sheet load image
sprite_sheet_image = pygame.image.load("sprites/player/megaman-sprite1.png").convert_alpha()
sprite_sheet = sprites.SpriteSheet(sprite_sheet_image)


player1 = Player(100,100, sprite_sheet, 5)

# move variables
moving_left = False
moving_right = False

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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("red")
    player1.get_input(moving_right, moving_left)
    player1.draw(screen)
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()