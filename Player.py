import pygame
import math
from Projectile import Projectile

PLAYERCOLOR = (255,   0,   0)

def normalize_vector(vector):
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)

class Player(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, screenSize):
        super().__init__()
        self.image = pygame.Surface([8, 8])
        self.image.fill(PLAYERCOLOR)
        self.rect = self.image.get_rect(x=screenSize[0]//2,
                                        y=screenSize[1]//2)
        
        self.pos = [screenSize[0] // 2, screenSize[1] // 2]
        self.health = 3
        self.alive = True
        self.movementVector = [0, 0]
        self.movementSpeed = 3
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 200

    def move(self, screenSize, tDelta):
        if self.movementVector != [0, 0]:
            self.movementVector = normalize_vector(self.movementVector)
        newPos = (self.pos[0] + self.movementVector[0]*self.movementSpeed*tDelta,
                  self.pos[1] + self.movementVector[1]*self.movementSpeed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
        elif newPos[0] > screenSize[0] - self.rect.width:
            self.pos[0] = screenSize[0] - self.rect.width
        else:
            self.pos[0] = newPos[0]

        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > screenSize[1]-self.rect.height:
            self.pos[1] = screenSize[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]
        
        self.rect.topleft = self.pos
        self.movementVector = [0, 0]
    def shoot(self, mousePos):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.weaponCooldown:
            direction = (mousePos[0] - self.pos[0], mousePos[1] - self.pos[1]) \
                if mousePos != self.pos else (1, 1)
            self.lastShot = currentTime
            self.projectiles.add(Projectile(self.pos,
                                            normalize_vector(direction),
                                            5, 2000, (0, 0, 255)))
    def render(self, surface):
        surface.blit(self.image, self.pos)
