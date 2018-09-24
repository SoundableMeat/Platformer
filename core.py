import pygame, random, time, math, numpy as np
from man import *
from animations import walk
from pygame.locals import *
from levels import *

pygame.init()
game=True
gameover=0
while game:

    screen = pygame.display.set_mode(size, FULLSCREEN)
    pygame.display.set_caption("PlayerMan")

    player = PlayerMan(PLAYERWIDTH, PLAYERHEIGHT)
    player_sprites, platforms, biggerplat, enemies, models = level1(player)

    background = pygame.transform.scale(pygame.image.load("sprites/bakgrunn.png").convert_alpha(),(SCREENWIDTH,SCREENHEIGHT))

    walkr, walkl = walkrl()

    clock = pygame.time.Clock()
    pygame.mixer.music.load("sound/hunted.mp3")
    #pygame.mixer.music.play()
    myfont = pygame.font.SysFont("monospace", 20)

    while carryOn: #Main loop

        if carryOn: #Starting conditions for frame
            screen.blit(background, (0, 0))

            for event in pygame.event.get(): #user did something
                if event.type == pygame.QUIT: #user clicked close
                    carryOn = False #end game
                    game=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: #user clicked escape
                        carryOn=False
                        game=False

            keys = pygame.key.get_pressed()

            plat_collision = pygame.sprite.spritecollide(player,biggerplat,False)

        if onBox: #Cheack if player falls of block
            for box in plat_collision:
                if player.rect.left>box.rect.right-13 or player.rect.right<box.rect.left+13:
                    onBox=False
                    jumping=True

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
            if player.verspeed<-player.rect.x:
                player.verspeed=-player.rect.x

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
                if player.verspeed<-player.rect.x:
                    player.verspeed=-player.rect.x

        for box in plat_collision: #Cheach collisions with boxes
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
                        player.rect.y = box.rect.top+13 - PLAYERHEIGHT
                        player.speed=0
                        jumping=False
                        onBox=True
            if player.rect.right==box.rect.right+13 or player.rect.left==box.rect.left-13:
                if player.speed>4:
                    player.speed-=0.5


        for enemy in enemies: #Move enemies
            if enemy.rect.x < SCREENWIDTH:
                plat_enemy = pygame.sprite.spritecollide(enemy,platforms,False)
                if plat_enemy==[]:
                    enemy.fall(0.35)
                else:
                    for box in plat_enemy:
                        if enemy.rect.right>box.rect.right and enemy.verspeed>0:
                            enemy.verspeed*=-1
                        elif enemy.rect.left<box.rect.left and enemy.verspeed<0:
                            enemy.verspeed*=-1

        if player.rect.right>=3*SCREENWIDTH/4: #Moving screen when at the end of it
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

        player.move() #Moves player
        for enemy in enemies: #Moves enemies
            enemy.move()

        enemy_hits = pygame.sprite.spritecollide(player,enemies,False) #Enemies in hitbox

        #for enemy in enemy_hits: #Game over if enemycollision
        #    carryOn=False

        #Drawing screen
        #biggerplat.update()
        #biggerplat.draw(screen)
        enemies.update() #Update enemies
        enemies.draw(screen) #Render enemies
        player_sprites.update() #Update playerman
        player_sprites.draw(screen) #Render playerman
        platforms.update() #Update platforms
        platforms.draw(screen) #Render platforms
        pygame.draw.rect(screen,BLACK,[0,0,100,50]) #Draw rectangle in corner
        models.draw(screen) #Render playerman in corner
        label = myfont.render("x {}".format(3-gameover), 1, WHITE) # render text in corner
        screen.blit(label, (50, 15)) #Render text in corner


        pygame.display.flip() #update screen

        clock.tick(60) #limits to 60 fps
    gameover+=1
    if gameover>3: #If i die 4 times game ends
        game=False
pygame.quit()
