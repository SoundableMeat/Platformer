import pygame
from man import *
from pygame.locals import *



def walkrl(PLAYERWIDTH, PLAYERHEIGHT):
    walkr = (pygame.transform.scale(pygame.image.load("playerman/walkr1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

    walkl = (pygame.transform.scale(pygame.image.load("playerman/walkl1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

    return walkr,walkl

def initialize_menu(SCREENWIDTH):
    menu_sprites=pygame.sprite.Group()

    man=PlayerMan(200, 200)
    man.rect.x=SCREENWIDTH/2-100
    man.rect.y=100
    menu_sprites.add(man)



    return menu_sprites

def level1(player,SCREENWIDTH,SCREENHEIGHT,PLAYERWIDTH, PLAYERHEIGHT):
    player_sprites = pygame.sprite.Group()
    player.rect.x = 200
    player.rect.y = SCREENHEIGHT-300
    player_sprites.add(player)

    platforms = pygame.sprite.Group()
    plat1 = Platform(500,40)
    plat1.rect.x = SCREENWIDTH/2
    plat1.rect.y = 10*SCREENHEIGHT/16
    plat2 = Platform(500,40)
    plat2.rect.x = 0
    plat2.rect.y = 7*SCREENHEIGHT/16
    floor = Floor(SCREENWIDTH*10,100)
    floor.rect.x = 0
    floor.rect.y = SCREENHEIGHT - 100
    """wall = Wall(40,SCREENHEIGHT)
    wall.rect.x=SCREENWIDTH/2 + 570
    wall.rect.y=0"""
    platforms.add(plat1)
    platforms.add(plat2)
    platforms.add(floor)
    #platforms.add(wall)

    biggerplat = pygame.sprite.Group()
    bigplat1 = Platform(526,66)
    bigplat1.rect.x = plat1.rect.x - 13
    bigplat1.rect.y = plat1.rect.y - 13
    bigplat2 = Platform(526,66)
    bigplat2.rect.x = plat2.rect.x - 13
    bigplat2.rect.y = plat2.rect.y - 13
    bigfloor = Floor(SCREENWIDTH*10,100)
    bigfloor.rect.x = 0
    bigfloor.rect.y = SCREENHEIGHT - 113
    """bigwall = Wall(66,SCREENHEIGHT)
    bigwall.rect.x = wall.rect.x-13
    bigwall.rect.y = wall.rect.y"""
    biggerplat.add(bigplat1)
    biggerplat.add(bigplat2)
    biggerplat.add(bigfloor)
    #biggerplat.add(bigwall)

    enemies = pygame.sprite.Group()
    enemy1 = EnemyMan(PLAYERWIDTH, PLAYERHEIGHT)
    enemy1.rect.x = 3*SCREENWIDTH/4
    enemy1.rect.y = 9*SCREENHEIGHT/16-10
    enemy1.verspeed = 4
    enemies.add(enemy1)

    models=pygame.sprite.Group()
    model=PlayerMan(30, 30)
    model.rect.x=5
    model.rect.y=10
    models.add(model)

    return player_sprites, platforms, biggerplat, enemies, models
