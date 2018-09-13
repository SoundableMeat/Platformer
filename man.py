import pygame
import math

WHITE = (255,255,255)

class PlayerMan(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load("playerman/walkr2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.hp = 100
        self.speed = 0
        self.verspeed = 0

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def moveRight(self, pixels):
        self.rect.x += pixels
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    def move(self):
        self.rect.x += self.verspeed
    def fall(self, change):
        self.speed = self.speed + change
        self.rect.y += self.speed

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
