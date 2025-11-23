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
            projectionHeight = (setting.tileSize) * ((setting.screenX / 2) / (math.tan(setting.FOV / 2))) / ray.rayDistance
            # wallColor = (255 - min(255, ray.rayDistance * 0.5), 0, 0)
            # pygame.draw.rect(display, wallColor, (setting.screenX + i * setting.resolution, (setting.screenY // 2) - (projectionHeight // 2), setting.resolution, projectionHeight))
            if ray.finalIsHorizontal:
                textureX = int((ray.wallHitX % setting.tileSize) / setting.tileSize * rayTexture.wall.width)
            elif ray.finalIsVertical:
                textureX = int((ray.wallHitY % setting.tileSize) / setting.tileSize * rayTexture.wall.width)
            
            textureX = max(0, min(textureX, rayTexture.wall.width - 1))
            tempTexture = pygame.transform.scale(rayTexture.wall.stripTextures[textureX], (setting.resolution, projectionHeight * rayTexture.wall.floorMultiplier))
            display.blit(tempTexture, (setting.screenX + i * setting.resolution, (setting.screenY // 2) - (tempTexture.get_height() - projectionHeight // 2) + self.player.z * projectionHeight * 0.01 ))
                