import pygame
from man import *
from pygame.locals import *

BLACK, WHITE, GREEN, RED, BLUE, YELLOW = (0,0,0), (255,255,255), (0,255,0), (255,0,0), (0,0,255), (255,255,0)
PLAYERWIDTH, PLAYERHEIGHT = 60,60
SCREENWIDTH,SCREENHEIGHT = 1366,768
walking = [0,0]
imagenum = [0,0]
size = (SCREENWIDTH,SCREENHEIGHT)
jumping = True
carryOn = True #game will carry on until False
onBox = False

def walkrl():
    walkr = (pygame.transform.scale(pygame.image.load("playerman/walkr1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

    walkl = (pygame.transform.scale(pygame.image.load("playerman/walkl1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
    pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

    return walkr,walkl

def level1(player):
    player_sprites = pygame.sprite.Group()

    player.rect.x = 200
    player.rect.y = SCREENHEIGHT-300
    player_sprites.add(player)

    platforms = pygame.sprite.Group()
    plat1 = Platform(500,40)
    plat1.rect.x = SCREENWIDTH/2
    plat1.rect.y = 10*SCREENHEIGHT/16
    floor = Floor(SCREENWIDTH,100)
    floor.rect.x = 0
    floor.rect.y = SCREENHEIGHT - 100
    platforms.add(plat1)
    platforms.add(floor)

    biggerplat = pygame.sprite.Group()
    bigplat1 = Platform(526,66)
    bigplat1.rect.x = plat1.rect.x - 13
    bigplat1.rect.y = plat1.rect.y - 13
    bigfloor = Floor(SCREENWIDTH,100)
    bigfloor.rect.x = 0
    bigfloor.rect.y = SCREENHEIGHT - 113
    biggerplat.add(bigplat1)
    biggerplat.add(bigfloor)

    enemies = pygame.sprite.Group()
    enemy1 = EnemyMan(PLAYERWIDTH, PLAYERHEIGHT)
    enemy1.rect.x = 3*SCREENWIDTH/4
    enemy1.rect.y = 9*SCREENHEIGHT/16
    enemy1.verspeed = 4
    enemies.add(enemy1)

    models=pygame.sprite.Group()
    model=PlayerMan(30, 30)
    model.rect.x=5
    model.rect.y=10
    models.add(model)

    return player_sprites, platforms, biggerplat, enemies, models
