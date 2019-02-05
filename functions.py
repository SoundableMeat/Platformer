import pygame, random, time, math, numpy as np
from man import *
from pygame.locals import *
from levels import *

def platform_col(player,box,keys):
    if player.rect.bottom>box.rect.top+13 and player.rect.top<box.rect.bottom-13:
        if player.verspeed>0 and player.rect.left<box.rect.left-46: #If playerman is left of box, meaning his left side is outside of left side of box plus 59 pixels
            if player.verspeed>box.rect.left+13-player.rect.right:
                player.verspeed=box.rect.left+13-player.rect.right
        elif player.verspeed<0 and player.rect.right>box.rect.right+46: #If playerman is right of box, meaning his right side is outside of right side of box plus 59 pixels
            if player.verspeed<box.rect.right-13-player.rect.left:
                player.verspeed=box.rect.right-13-player.rect.left
    if player.rect.right>box.rect.left+13 and player.rect.left<box.rect.right-13:
        if player.speed<0 and player.rect.bottom>box.rect.bottom:
            if player.speed<box.rect.bottom-13-player.rect.top:
                player.speed=box.rect.bottom-13-player.rect.top
        elif player.speed>0 and player.rect.top<box.rect.top:
            if player.speed>box.rect.top+13-player.rect.bottom:
                player.rect.y = box.rect.top+13 - player.height
                player.speed=0
                player.jumping=False
                player.onBox=True
    if player.rect.right>=box.rect.right+12:
        if player.speed>4:
            player.speed-=0.5
        if keys[pygame.K_SPACE] and player.speed<=4 and player.speed>0:
            player.speed=-13
            player.verspeed=10
    elif player.rect.left<=box.rect.left-12:
        if player.speed>4:
            player.speed-=0.5
        if keys[pygame.K_SPACE] and player.speed<=4 and player.speed>0:
            player.speed=-13
            player.verspeed=-10

def ground_movement(keys,walk,player,walkl,walkr):
    if keys:
        if keys[pygame.K_SPACE]: #Cheack player.jumping
            player.speed = -13
            player.jumping=True
            player.onBox=False
        if keys[pygame.K_z]: #Cheak sprinting
            sprint=True
        else:
            sprint=False
        if sprint==True: #Sprinting machanics
            if keys[pygame.K_RIGHT]: #Cheack walking
                walk(keys, player, walkr, walkl, player.walking,player.imagenum,sprint)
                if player.verspeed<0:
                    player.verspeed+=0.7
                elif player.verspeed<10:
                    player.verspeed+=0.3
            elif keys[pygame.K_LEFT]:
                walk(keys, player, walkr, walkl, player.walking,player.imagenum,sprint)
                if player.verspeed>0:
                    player.verspeed-=0.7
                elif player.verspeed>-10:
                    player.verspeed-=0.3
            else:
                if player.image in walkl:
                    player.image = walkl[1]
                elif player.image in walkr:
                    player.image = walkr[1]
        else: #player.walking mechanics
            if keys[pygame.K_RIGHT]: #Cheack player.walking
                walk(keys, player, walkr, walkl, player.walking,player.imagenum,sprint)
                if player.verspeed<0:
                    player.verspeed+=0.5
                elif player.verspeed<5:
                    player.verspeed+=0.2
            elif keys[pygame.K_LEFT]:
                walk(keys, player, walkr, walkl, player.walking,player.imagenum,sprint)
                if player.verspeed>0:
                    player.verspeed-=0.5
                elif player.verspeed>-5:
                    player.verspeed-=0.2
            else:
                if player.image in walkl:
                    player.image = walkl[1]
                elif player.image in walkr:
                    player.image = walkr[1]
        if player.verspeed<-player.rect.x:
            player.verspeed=-player.rect.x
    if abs(player.verspeed)>0:
        if not keys[pygame.K_RIGHT]:
            if not keys[pygame.K_LEFT]:
                if player.verspeed>0.7:
                    player.verspeed-=0.7
                elif player.verspeed<-0.7:
                    player.verspeed+=0.7
                else:
                    player.verspeed=0

def jump(player,keys,walkl,walkr):
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
                player.verspeed+=0.3
        elif abs(player.verspeed)<10:
            if keys[pygame.K_RIGHT]:
                player.verspeed+=0.3
            elif keys[pygame.K_LEFT]:
                player.verspeed-=0.3
        else:
            if keys[pygame.K_LEFT]:
                player.verspeed-=0.3
    if player.verspeed<-player.rect.x:
        player.verspeed=-player.rect.x

def addbullet(player,walkl,walkr):
    bullet = Projectile(5,player,walkl,walkr)
    if player.image in walkr:
        bullet.speed = 20
        bullet.rect.x = player.rect.x+player.width/2
    elif player.image in walkl:
        bullet.speed = -20
        bullet.rect.x = player.rect.x+20
    bullet.rect.y=player.rect.y+player.height/2
    return bullet

def move_screen(player,platforms,biggerplat,enemies,SCREENWIDTH):
    player.rect.x-=abs(player.verspeed)
    for plat in platforms:
        plat.rect.x-=abs(player.verspeed)
        if plat.rect.right<0:
            plat.kill()
    for enemy in enemies:
        enemy.rect.x-=abs(player.verspeed)
        if enemy.rect.right<=-SCREENWIDTH/3:
            enemy.kill()
    for box in biggerplat:
        box.rect.x-=abs(player.verspeed)
        if box.rect.right<0:
            box.kill()
