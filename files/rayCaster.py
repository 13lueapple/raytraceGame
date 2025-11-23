import pygame, math
import setting, rayTexture
from rayPlayer import Player
from ray import Ray
from rayMap import Map
from util import *



class RayCaster:
    def __init__(self, player, map):
        self.rays = []
        self.player: Player = player
        self.map: Map = map
        
    def castAll(self):
        self.rays: list[Ray] = []
        self.rayAngle = self.player.angle - (setting.FOV / 2)
        for _ in range(setting.rayNumber):
            ray = Ray(self.rayAngle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)
            self.rayAngle += setting.FOV / setting.rayNumber
            
    def drawAll(self, display: pygame.Surface):
        for i, ray in enumerate(self.rays):
            ray.draw(display)
            projectionHeight = (32) * ((setting.screenX / 2) / (math.tan(setting.FOV / 2))) / ray.rayDistance
            # wallColor = (255 - min(255, ray.rayDistance * 0.5), 0, 0)
            # pygame.draw.rect(display, wallColor, (setting.screenX + i * setting.resolution, (setting.screenY // 2) - (projectionHeight // 2), setting.resolution, projectionHeight))
            if ray.finalIsHorizontal:
                textureX = int((ray.wallHitX % setting.tileSize) / setting.tileSize * rayTexture.texture1.get_width())
                textureX = max(0, min(textureX, rayTexture.texture1.get_width() - 1))
                display.blit(pygame.transform.scale(rayTexture.texture1Strip[textureX], (setting.resolution, projectionHeight)), (setting.screenX + i * setting.resolution, (setting.screenY // 2) - (projectionHeight // 2)))
            elif ray.finalIsVertical:
                textureX = int((ray.wallHitY % setting.tileSize) / setting.tileSize * rayTexture.texture1.get_width())
                textureX = max(0, min(textureX, rayTexture.texture1.get_width() - 1))
                display.blit(pygame.transform.scale(rayTexture.texture1Strip[textureX], (setting.resolution, projectionHeight)), (setting.screenX + i * setting.resolution, (setting.screenY // 2) - (projectionHeight // 2)))
