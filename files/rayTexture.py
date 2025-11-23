import pygame
import setting

pygame.init()

def loadTexture(path, rayNumber):
    return pygame.transform.scale(pygame.image.load(path).convert(), (rayNumber, rayNumber))

def stripTexture(texture: pygame.Surface, rayNumber):
    textureStrip = []
    for x in range(texture.get_width()):
        strip = pygame.Surface((1, rayNumber))
        strip.blit(texture,(0,0), (x, 0, 1, rayNumber))
        textureStrip.append(strip)
    return textureStrip
    

texture1 = loadTexture("files/textures/grass.png", setting.rayNumber)
texture1Strip = stripTexture(texture1, setting.rayNumber)