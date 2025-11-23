import pygame, math
import setting
from rayMap import Map
from util import *
from rayPlayer import Player

class Ray:
    def __init__(self, angle, player, map):
        self.rayAngle = normalizeAngle(angle)
        self.player: Player = player
        
        self.isDown = self.rayAngle > 0 and self.rayAngle < math.pi
        self.isUp = not self.isDown
        self.isRight = self.rayAngle > 1.5 * math.pi or self.rayAngle < 0.5 * math.pi
        self.isLeft = not self.isRight
        
        self.wallHitX, self.wallHitY = 0, 0
        
        self.map: Map = map
        
        self.rayDistance = 0
        
        self.finalIsHorizontal = False
        self.finalIsVertical = False
    
    def cast(self):
        self.finalIsHorizontal = False
        self.finalIsVertical = False
        
        
        isHorizontalWall = False
        horizontalHitX, horizontalHitY = 0, 0
        
        firstIntersectionX, firstIntersectionY = None, None
        
        if self.isUp: firstIntersectionY = (self.player.y // setting.tileSize) * setting.tileSize - 1
        elif self.isDown: firstIntersectionY = (self.player.y // setting.tileSize) * setting.tileSize + setting.tileSize
    
        firstIntersectionX = (firstIntersectionY - self.player.y) / math.tan(self.rayAngle) + self.player.x    
    
        nextIntersectionX, nextIntersectionY = firstIntersectionX, firstIntersectionY
        dx, dy = 0, 0
        
        if self.isUp: dy = -setting.tileSize
        elif self.isDown: dy = setting.tileSize
        dx = dy / math.tan(self.rayAngle)
        
        while (nextIntersectionX < setting.screenX and nextIntersectionX >= 0 and nextIntersectionY < setting.screenY and nextIntersectionY >= 0):
            if self.map.isWall(nextIntersectionX, nextIntersectionY):
                isHorizontalWall = True
                horizontalHitX, horizontalHitY = nextIntersectionX, nextIntersectionY
                break
            else:
                nextIntersectionX += dx
                nextIntersectionY += dy
        
        isVerticalWall = False
        verticalHitX, verticalHitY = 0, 0
        
        if self.isLeft: firstIntersectionX = (self.player.x // setting.tileSize) * setting.tileSize - 1
        elif self.isRight: firstIntersectionX = (self.player.x // setting.tileSize) * setting.tileSize + setting.tileSize
        
        firstIntersectionY = (firstIntersectionX - self.player.x) * math.tan(self.rayAngle) + self.player.y
        nextIntersectionX, nextIntersectionY = firstIntersectionX, firstIntersectionY
        dx, dy = 0, 0
        
        if self.isLeft: dx = -setting.tileSize
        elif self.isRight: dx = setting.tileSize
        dy = dx * math.tan(self.rayAngle)
        
        while (nextIntersectionX < setting.screenX and nextIntersectionX >= 0 and nextIntersectionY < setting.screenY and nextIntersectionY >= 0):
            if self.map.isWall(nextIntersectionX, nextIntersectionY):
                isVerticalWall = True
                verticalHitX, verticalHitY = nextIntersectionX, nextIntersectionY
                break
            else:
                nextIntersectionX += dx
                nextIntersectionY += dy
        
        
        horizontalDistance = math.inf
        verticalDistance = math.inf
        
        if isHorizontalWall:
            horizontalDistance = distanceBetweenPoints(self.player.x, self.player.y, horizontalHitX, horizontalHitY)
        if isVerticalWall:
            verticalDistance = distanceBetweenPoints(self.player.x, self.player.y, verticalHitX, verticalHitY)
            
        if horizontalDistance < verticalDistance:
            self.wallHitX, self.wallHitY = horizontalHitX, horizontalHitY
            self.finalIsHorizontal = True
        else:
            self.wallHitX, self.wallHitY = verticalHitX, verticalHitY
            self.finalIsVertical = True
        
        self.rayDistance = distanceBetweenPoints(self.player.x, self.player.y, self.wallHitX, self.wallHitY) * (math.cos(self.player.angle- self.rayAngle))
        if self.rayDistance < 1: self.rayDistance = 1
        
    def draw(self, display):
        pygame.draw.line(display, self.player.color, (self.player.x, self.player.y),(self.wallHitX, self.wallHitY)) 
        