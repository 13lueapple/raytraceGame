import pygame, math
import setting
from rayMap import Map

class Player:
    def __init__(self, map):
        self.color = (255,255,0)
        self.x, self.y = setting.screenX//2, setting.screenY//2
        self.size = 5
        self.angle = -90 * (math.pi / 180)
        self.moveSpeed = 2
        self.angleSpeed = 1 * (math.pi / 180)
        self.moveDirection = 0
        self.rotateDirection = 0
        self.directionLineLength = 10
        self.directionLineColor = (255,0,0)
        self.map: Map = map
        
    def getPos(self):
        return self.x, self.y
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        self.moveDirection = 0
        self.rotateDirection = 0
        
        if keys[pygame.K_w]: self.moveDirection = 1
        if keys[pygame.K_s]: self.moveDirection = -1
        if keys[pygame.K_a]: self.rotateDirection = -1
        if keys[pygame.K_d]: self.rotateDirection = 1
            
        self.angle += self.angleSpeed * self.rotateDirection
        if self.map.isWall(self.x + math.cos(self.angle) * self.moveDirection * self.moveSpeed, self.y) == False:
            self.x += math.cos(self.angle) * self.moveDirection * self.moveSpeed
        if self.map.isWall(self.x, self.y + math.sin(self.angle) * self.moveDirection * self.moveSpeed) == False:
            self.y += math.sin(self.angle) * self.moveDirection * self.moveSpeed
    
    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size)

        pygame.draw.line(display, self.directionLineColor, (self.x, self.y), (self.x + math.cos(self.angle) * self.directionLineLength, self.y + math.sin(self.angle) * self.directionLineLength))
