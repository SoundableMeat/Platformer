import pygame
from man import PlayerMan

def walk(keys, player, walkr, walkl,walking,image,sprint):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if player.image in walkl:
            player.image=walkr[1]
        if sprint==False:
            walking[0]+=1
        if sprint==True:
            walking[0]+=2

        if walking[0]>=10:
            if image[0]<3:
                image[0]+=1
            else:
                image[0]=0
            player.image=walkr[image[0]]
            walking[0]=0

    elif keys[pygame.K_LEFT]:
        if player.image in walkr:
            player.image=walkl[1]
        if sprint==False:
            walking[1]+=1
        if sprint==True:
            walking[1]+=2

        if walking[1]>=10:
            if image[1]<3:
                image[1]+=1
            else:
                image[1]=0
            player.image=walkl[image[1]]
            walking[1]=0
