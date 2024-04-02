import pygame
from player import *

TILESIZE = 120
level_data = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
    [-1,-1,-1,2,2,2,1,-1,2,-1,-1,-1,2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]]       


                

class World():
    def __init__(self):
        self.obastabcle_list = []


    def process_data(self, data, grass_image, sprite_sheet1, sprite_sheet2, enemy_sheet1, enemy_sheet2,enemy_group):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_rect = grass_image.get_rect()
                    img_rect.x = x * TILESIZE
                    img_rect.y = y * TILESIZE
                    tile_data = (grass_image, img_rect)
                    # creategrass block
                    if tile == 0:
                        self.obastabcle_list.append(tile_data)
                    # create player
                    if tile == 1:
                        player1 = Player("player", (x*TILESIZE,y*TILESIZE), sprite_sheet1, sprite_sheet2, 7)
                    # create enemy
                    if tile == 2:
                        enemy1 = Player("enemy", (x*TILESIZE,y*TILESIZE), enemy_sheet1, enemy_sheet2, 4)
                        enemy_group.add(enemy1)
                        
        return player1, enemy_group
    
    def draw(self,screen, screen_scroll, player1):
        for tile in self.obastabcle_list:
            if player1.alive:
                tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

