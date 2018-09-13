import pygame, random, time, math, numpy as np
from man import *
from animations import walk
from pygame.locals import *

pygame.init()

BLACK, WHITE, GREEN, RED, BLUE, YELLOW = (0,0,0), (255,255,255), (0,255,0), (255,0,0), (0,0,255), (255,255,0)
speedx, speedy = 1,1
walking = [0,0]
imagenum = [0,0]

SCREENWIDTH,SCREENHEIGHT = 1366,768
PLAYERWIDTH, PLAYERHEIGHT = 60,60
size = (SCREENWIDTH,SCREENHEIGHT)
screen = pygame.display.set_mode(size, FULLSCREEN)
pygame.display.set_caption("PlayerMan")

player_sprites = pygame.sprite.Group()
player = PlayerMan(PLAYERWIDTH, PLAYERHEIGHT)
player.rect.x = SCREENWIDTH/2
player.rect.y = SCREENHEIGHT/2
player_sprites.add(player)

obst_sprites = pygame.sprite.Group()
leftwall = Wall(20,SCREENHEIGHT)
leftwall.rect.x = 0
leftwall.rect.y = 0
rightwall = Wall(20,SCREENHEIGHT)
rightwall.rect.x = SCREENWIDTH-20
rightwall.rect.y = 0
roof = Roof(SCREENWIDTH,20)
roof.rect.x = 0
roof.rect.y = 0
floor = Floor(SCREENWIDTH,100)
floor.rect.x = 0
floor.rect.y = SCREENHEIGHT - 100
obst_sprites.add(leftwall)
obst_sprites.add(rightwall)
obst_sprites.add(roof)
obst_sprites.add(floor)

platforms = pygame.sprite.Group()
plat1 = Platform(150,40)
plat1.rect.x = SCREENWIDTH - SCREENWIDTH/7
plat1.rect.y = SCREENHEIGHT - SCREENHEIGHT/5
platforms.add(plat1)

background = pygame.transform.scale(pygame.image.load("sprites/bakgrunn.png").convert_alpha(),(SCREENWIDTH,SCREENHEIGHT))

walkr = (pygame.transform.scale(pygame.image.load("playerman/walkr1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

walkl = (pygame.transform.scale(pygame.image.load("playerman/walkl1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

carryOn = True #game will carry on until False
clock = pygame.time.Clock()

while carryOn:

    screen.blit(background, (0, 0))

    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT: #user clicked close
            carryOn = False #end game
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: #user clicked escape
                carryOn=False

    keys = pygame.key.get_pressed()

    collision_list = pygame.sprite.spritecollide(player,obst_sprites,False)
    plat_collision = pygame.sprite.spritecollide(player,platforms,False)

    if keys: #Walkinng algorythm
        if keys[pygame.K_SPACE]: #Cheack jumping
            if floor in collision_list:
                player.rect.y = floor.rect.y - PLAYERHEIGHT-3
                player.speed = -10
                player.fall(0.1)

        if keys[pygame.K_z]: #Cheak sprinting
            sprint=True
        else:
            sprint=False

        if floor in collision_list:
            if keys[pygame.K_RIGHT]: #Cheack walking
                walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                if sprint==True:
                    player.verspeed=10
                else:
                    player.verspeed=5
            elif keys[pygame.K_LEFT]:
                walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                if sprint==True:
                    player.verspeed=-10
                else:
                    player.verspeed=-5
            else:
                if player.image in walkl:
                    player.image = walkl[1]
                elif player.image in walkr:
                    player.image = walkr[1]
                player.verspeed=0
        else:
            if player.verspeed>0:
                player.image = walkr[2]
            if player.verspeed<0:
                player.image = walkl[0]

    if player.verspeed>0 and rightwall in collision_list:
        player.verspeed=0
    if player.verspeed<0 and leftwall in collision_list:
        player.verspeed=0

    player.move()

    if floor not in collision_list:
        if player.speed<10:
            player.fall(0.35)
        else:
            player.fall(0)

    #Drawing screen
    player_sprites.update()
    player_sprites.draw(screen)
    obst_sprites.update()
    obst_sprites.draw(screen)
    platforms.update()
    platforms.draw(screen)

    pygame.display.flip() #update screen

    clock.tick(60) #limits to 60 fps

pygame.quit()
