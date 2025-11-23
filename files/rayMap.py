import pygame
from setting import *

class Map:
    def __init__(self):
        self.content = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                        [1,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1],
                        [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
                        [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1],
                        [1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        ]
    
    def isWall(self, x, y):
        return self.content[int(y // tileSize)][int(x // tileSize)] == 1
    
    def draw(self, display: pygame.Surface):
        for i in range(len(self.content)):
            for j in range(len(self.content[0])):
                tileX = tileSize * j
                tileY = tileSize * i
                if self.content[i][j] == 1:
                    pygame.draw.rect(display, (50,50,50), (tileX, tileY, tileSize - 1, tileSize - 1))
                else:
                    pygame.draw.rect(display, (0,0,0), (tileX, tileY, tileSize - 1, tileSize - 1))
