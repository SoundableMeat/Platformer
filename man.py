import pygame
import math

WHITE = (255,255,255)

class PlayerMan(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("playerman/walkr2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.speed = 0
        self.verspeed = 0
        self.jumping=True
        self.onBox=False
        self.height=height
        self.width=width
        self.walking = [0,0]
        self.imagenum = [0,0]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x += self.verspeed
    def fall(self, change):
        self.speed += change
        self.rect.y += self.speed

class EnemyMan(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("playerman/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.speed = 0
        self.verspeed = 0
        self.hp = 3

        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x += self.verspeed
    def fall(self, change):
        self.speed += change
        self.rect.y += self.speed
    def get_hit(self,player):
        if player.rect.x<self.rect.x:
            self.verspeed = abs(self.verspeed)
        elif player.rect.x>self.rect.x:
            self.verspeed = -abs(self.verspeed)
        self.speed -= 7
        self.hp-=1

class Floor(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("sprites/floor.png").convert()
        self.image = pygame.transform.scale(self.image, (width,height))

        self.rect = self.image.get_rect()

class Wall(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("sprites/wall.png").convert()
        self.image = pygame.transform.scale(self.image, (width,height))

        self.rect = self.image.get_rect()

class Roof(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("sprites/roof.png").convert()
        self.image = pygame.transform.scale(self.image, (width,height))

        self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("sprites/platform.png").convert()
        self.image = pygame.transform.scale(self.image, (width,height))

        self.rect = self.image.get_rect()

class Projectile(pygame.sprite.Sprite):

    def __init__(self, rad, player, walkl, walkr):

        super().__init__()

        self.image = pygame.Surface((rad,rad))
        #self.image = pygame.draw.circle(pygame.Surface((rad,rad)),rad)
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x += self.speed
