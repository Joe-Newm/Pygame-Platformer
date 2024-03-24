# Example file showing a basic pygame "game loop"
import pygame
import player
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

frame0 = sprite_sheet.get_image(23, 25, 4)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("red")

    # RENDER YOUR GAME HERE
    screen.blit(frame0, (200,200))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()