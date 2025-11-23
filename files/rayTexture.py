import pygame
import setting

class textureLoader:
    def __init__(self, path):
        self.texture = pygame.transform.scale(pygame.image.load(path).convert(), (setting.rayNumber, setting.rayNumber))
        self.stripTextures = []
        self.width, self.height = self.texture.get_width(), self.texture.get_height()
    
    def strip(self, floorMultiplier = 1):
        self.floorMultiplier = floorMultiplier
        for x in range(self.width):
            strip = pygame.Surface((1, setting.rayNumber * self.floorMultiplier))
            for i in range(self.floorMultiplier):
                strip.blit(self.texture,(0,setting.rayNumber * i), (x, 0, 1, setting.rayNumber))
            self.stripTextures.append(strip)
        

wall = textureLoader("files/textures/grass.png")
wall.strip(3)