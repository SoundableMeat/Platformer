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
player.rect.x = 200
player.rect.y = SCREENHEIGHT-300
player_sprites.add(player)

obst_sprites = pygame.sprite.Group()
leftwall = Wall(20,SCREENHEIGHT)
leftwall.rect.x = 0
leftwall.rect.y = 0
"""rightwall = Wall(20,SCREENHEIGHT)
rightwall.rect.x = SCREENWIDTH-20
rightwall.rect.y = 0"""
roof = Roof(SCREENWIDTH,20)
roof.rect.x = 0
roof.rect.y = 0
floor = Floor(SCREENWIDTH,100)
floor.rect.x = 0
floor.rect.y = SCREENHEIGHT - 100
obst_sprites.add(leftwall)
#obst_sprites.add(rightwall)
obst_sprites.add(roof)
obst_sprites.add(floor)

platforms = pygame.sprite.Group()
plat1 = Platform(500,40)
plat1.rect.x = SCREENWIDTH/2
plat1.rect.y = 11*SCREENHEIGHT/16
platforms.add(plat1)

enemies = pygame.sprite.Group()
enemy1 = EnemyMan(PLAYERWIDTH, PLAYERHEIGHT)
enemy1.rect.x = 3*SCREENWIDTH/4
enemy1.rect.y = 9*SCREENHEIGHT/16
enemy1.verspeed = 4
enemies.add(enemy1)

background = pygame.transform.scale(pygame.image.load("sprites/bakgrunn.png").convert_alpha(),(SCREENWIDTH,SCREENHEIGHT))

walkr = (pygame.transform.scale(pygame.image.load("playerman/walkr1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkr2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

walkl = (pygame.transform.scale(pygame.image.load("playerman/walkl1.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl3.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)),
pygame.transform.scale(pygame.image.load("playerman/walkl2.png").convert_alpha(), (PLAYERWIDTH, PLAYERHEIGHT)))

#onBlock = False
jumping = True
carryOn = True #game will carry on until False
onBox = False
clock = pygame.time.Clock()
pygame.mixer.music.load("sound/hunted.mp3")
#pygame.mixer.music.play()

while carryOn:

    if carryOn:
        screen.blit(background, (0, 0))

        for event in pygame.event.get(): #user did something
            if event.type == pygame.QUIT: #user clicked close
                carryOn = False #end game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #user clicked escape
                    carryOn=False

        keys = pygame.key.get_pressed()

        collision_list = pygame.sprite.spritecollide(player,obst_sprites,False)
        plat_collision = pygame.sprite.spritecollide(player,platforms,False) #Initializing loop

    for box in plat_collision: #If player hit top of box he stops in y-direction and stands on box
        if player.rect.center[1]<box.rect.y and player.rect.right>box.rect.x and player.rect.left<box.rect.right:
            jumping=False
            onBox=True
            player.rect.y = box.rect.top - PLAYERHEIGHT
            player.speed=0

    if onBox: #Cheack if player falls of block
        if player.rect.right<box.rect.x or player.rect.left>box.rect.right:
            onBox=False
            jumping=True
    elif floor in collision_list: #Cheack if player is on ground
        jumping=False
        player.rect.y = floor.rect.top - PLAYERHEIGHT
    elif player.speed>(floor.rect.top-player.rect.bottom): #If player goes fast when going toward the ground, he slows down
        player.speed=floor.rect.top-player.rect.bottom+1


    if jumping: #Jumping animation and controlls
        if player.speed<10:
            player.fall(0.4)
        else:
            player.fall(0)
        if player.verspeed>0:
            player.image = walkr[2]
        elif player.verspeed<0:
            player.image = walkl[0]
        if keys:
            if player.verspeed<=-10:
                if keys[pygame.K_RIGHT]:
                    player.verspeed+=0.7
            elif abs(player.verspeed)<10:
                if keys[pygame.K_RIGHT]:
                    player.verspeed+=0.7
                elif keys[pygame.K_LEFT]:
                    player.verspeed-=0.7
            else:
                if keys[pygame.K_LEFT]:
                    player.verspeed-=0.7

    else: #Movement on ground
        if keys:
            if keys[pygame.K_SPACE]: #Cheack jumping
                player.speed = -13
                jumping=True
                onBox=False
            if keys[pygame.K_z]: #Cheak sprinting
                sprint=True
            else:
                sprint=False
            if sprint==True: #Sprinting machanics
                if keys[pygame.K_RIGHT]: #Cheack walking
                    walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                    player.verspeed=10
                elif keys[pygame.K_LEFT]:
                    walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                    player.verspeed=-10
                else:
                    if player.image in walkl:
                        player.image = walkl[1]
                    elif player.image in walkr:
                        player.image = walkr[1]
                    player.verspeed=0
            else: #Walking mechanics
                if keys[pygame.K_RIGHT]: #Cheack walking
                    walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                    player.verspeed=5
                elif keys[pygame.K_LEFT]:
                    walk(keys, player, walkr, walkl, walking,imagenum,sprint)
                    player.verspeed=-5
                else:
                    if player.image in walkl:
                        player.image = walkl[1]
                    elif player.image in walkr:
                        player.image = walkr[1]
                    player.verspeed=0 #Walking mechanics

    """if rightwall in collision_list and player.verspeed>0:
        player.verspeed=0"""
    if leftwall in collision_list and player.verspeed<0:
        player.verspeed=0
    for box in plat_collision:
        if player.rect.center[0]<box.rect.left and player.rect.bottom>box.rect.top and player.rect.top<box.rect.bottom and player.verspeed>0:
            player.verspeed=0
            if player.rect.x>box.rect.left-PLAYERWIDTH+1:
                player.rect.x-=2
        elif player.rect.center[0]>box.rect.right and player.rect.bottom>box.rect.top and player.rect.top<box.rect.bottom and player.verspeed<0:
            player.verspeed=0
            if player.rect.x<box.rect.right-1:
                player.rect.x+=2
        elif player.rect.center[1]>box.rect.bottom and player.rect.right>box.rect.x and player.rect.left<box.rect.right:
            if player.speed<0:
                player.speed=0

    for enemy in enemies:
        plat_enemy = pygame.sprite.spritecollide(enemy,platforms,False)
        if plat_enemy==[]:
            enemy.fall(0.35)
        else:
            for box in plat_enemy:
                if enemy.rect.right>box.rect.right and enemy.verspeed>0:
                    enemy.verspeed*=-1
                elif enemy.rect.left<box.rect.left and enemy.verspeed<0:
                    enemy.verspeed*=-1

    if player.rect.right>=3*SCREENWIDTH/4:
        player.rect.x-=abs(player.verspeed)
        for plat in platforms:
            plat.rect.x-=abs(player.verspeed)
        for enemy in enemies:
            enemy.rect.x-=abs(player.verspeed)


    player.move()
    for enemy in enemies:
        enemy.move()

    enemy_hits = pygame.sprite.spritecollide(player,enemies,False)

    for enemy in enemy_hits:
        player.rect.x = 200
        player.rect.y = SCREENHEIGHT-300
        player.speed=0
        player.verspeed=0

    #Drawing screen
    enemies.update()
    enemies.draw(screen)
    player_sprites.update()
    player_sprites.draw(screen)
    obst_sprites.update()
    obst_sprites.draw(screen)
    platforms.update()
    platforms.draw(screen)

    pygame.display.flip() #update screen

    clock.tick(60) #limits to 60 fps

pygame.quit()
