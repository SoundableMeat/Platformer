import pygame, random, time, math, numpy as np
from man import *
from animations import walk
from pygame.locals import *
from levels import *
from functions import *

pygame.init()
gameover=0
BLACK, WHITE, GREEN, RED, BLUE, YELLOW = (0,0,0), (255,255,255), (0,255,0), (255,0,0), (0,0,255), (255,255,0)
PLAYERWIDTH, PLAYERHEIGHT = 60,60
SCREENWIDTH,SCREENHEIGHT = 1366,768

menu=True

size = (SCREENWIDTH,SCREENHEIGHT)
carryOn = True #game will carry on until False

screen = pygame.display.set_mode(size, FULLSCREEN)
pygame.display.set_caption("PlayerMan")

background = pygame.transform.scale(pygame.image.load("sprites/bakgrunn.png").convert_alpha(),(SCREENWIDTH,SCREENHEIGHT))
clock = pygame.time.Clock()

menu_sprites=initialize_menu(SCREENWIDTH)

"""while menu:
    screen.blit(background, (0, 0))

    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT: #user clicked close
            carryOn = False #end game
            menu=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: #user clicked escape
                carryOn=False
                menu=False
            elif event.key==pygame.K_RETURN:
                menu=False

    menu_sprites.draw(screen)

    pygame.display.flip() #update screen

    clock.tick(60) #limits to 60 fps"""


player = PlayerMan(PLAYERWIDTH, PLAYERHEIGHT)
player_sprites, platforms, biggerplat, enemies, models = level1(player,SCREENWIDTH,SCREENHEIGHT,player.width, player.height)

walkr, walkl = walkrl(player.width, player.height)
player.image = walkr[1]

pygame.mixer.music.load("sound/hunted.mp3")
#pygame.mixer.music.play()
myfont = pygame.font.SysFont("monospace", 20)
bullets=pygame.sprite.Group()

while carryOn: #Main loop

    if carryOn: #Starting conditions for frame
        screen.blit(background, (0, 0))

        for event in pygame.event.get(): #user did something
            if event.type == pygame.QUIT: #user clicked close
                carryOn = False #end game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #user clicked escape
                    carryOn=False

        keys = pygame.key.get_pressed()

        plat_collision = pygame.sprite.spritecollide(player,biggerplat,False)

    if player.onBox: #Cheack if player falls of block
        for box in plat_collision:
            if player.rect.left>box.rect.right-13 or player.rect.right<box.rect.left+13:
                player.onBox=False
                player.jumping=True

    if player.jumping: #player.jumping animation and controlls
        jump(player,keys,walkl,walkr)

    else: #Movement on ground
        ground_movement(keys,walk,player,walkl,walkr)

    for box in plat_collision: #Cheach collisions with boxes
        platform_col(player,box,keys)

    if keys[pygame.K_f] and len(bullets)<1:
        bullet = addbullet(player,walkl,walkr)
        bullets.add(bullet)

    for bullet in bullets:
        if bullet.rect.x>SCREENWIDTH or bullet.rect.x<0:
            bullet.kill()

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
                    enemy.rect.y = box.rect.y-PLAYERHEIGHT+1
                    enemy.speed=0

    if player.rect.right>=3*SCREENWIDTH/4: #Moving screen when at the end of it
        move_screen(player,platforms,biggerplat,enemies,SCREENWIDTH)

    player.move() #Moves player
    for enemy in enemies: #Moves enemies
        enemy.move()
    for bullet in bullets:
        bullet.move()

    enemy_hits = pygame.sprite.spritecollide(player,enemies,False) #Enemies in hitbox

    for bullet in bullets:
        bullet_hits_enemy = pygame.sprite.spritecollide(bullet,enemies,False)
        bullet_hits_structure = pygame.sprite.spritecollide(bullet,platforms,False)
        for enemy in bullet_hits_enemy:
            if enemy.hp>1:
                enemy.get_hit(player)
                bullet.kill()
                enemy.fall(0.35)
            else:
                enemy.kill()
                bullet.kill()
        if len(bullet_hits_structure)>0:
            bullet.kill()

    for enemy in enemy_hits: #Game over if enemycollision
        carryOn=False

    #Drawing screen
    #biggerplat.update()
    #biggerplat.draw(screen)
    enemies.update() #Update enemies
    enemies.draw(screen) #Render enemies
    player_sprites.update() #Update playerman
    player_sprites.draw(screen) #Render playerman
    platforms.update() #Update platforms
    platforms.draw(screen) #Render platforms
    bullets.update()
    bullets.draw(screen)
    pygame.draw.rect(screen,BLACK,[0,0,100,50]) #Draw rectangle in corner
    models.draw(screen) #Render playerman in corner
    label = myfont.render("x {}".format(3-gameover), 1, WHITE) # render text in corner
    screen.blit(label, (50, 15)) #Render text in corner


    pygame.display.flip() #update screen

    clock.tick(60) #limits to 60 fps

pygame.quit()
