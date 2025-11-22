import pygame, math, sys

tileSize = 32
screenX = tileSize * 20
screenY = tileSize * 15

display = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()

FOV = 60 * (math.pi / 180)
resolution = 4
rayNumber = (screenX // resolution)

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0: angle += (2 * math.pi)
    return angle


def distanceBetweenPoints(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

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


class Player:
    def __init__(self, map):
        self.color = (255,255,0)
        self.x, self.y = screenX//2, screenY//2
        self.size = 5
        self.angle = -90 * (math.pi / 180)
        self.moveSpeed = 3
        self.angleSpeed = 3 * (math.pi / 180)
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
        self.x += math.cos(self.angle) * self.moveDirection * self.moveSpeed
        self.y += math.sin(self.angle) * self.moveDirection * self.moveSpeed
    
    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.size)

        pygame.draw.line(display, self.directionLineColor, (self.x, self.y), (self.x + math.cos(self.angle) * self.directionLineLength, self.y + math.sin(self.angle) * self.directionLineLength))

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
    
    def cast(self):
        isHorizontalWall = False
        horizontalHitX, horizontalHitY = 0, 0
        
        firstIntersectionX, firstIntersectionY = None, None
        
        if self.isUp: firstIntersectionY = (self.player.y // tileSize) * tileSize - 1
        elif self.isDown: firstIntersectionY = (self.player.y // tileSize) * tileSize + tileSize
    
        firstIntersectionX = (firstIntersectionY - self.player.y) / math.tan(self.rayAngle) + self.player.x    
    
        nextIntersectionX, nextIntersectionY = firstIntersectionX, firstIntersectionY
        dx, dy = 0, 0
        
        if self.isUp: dy = -tileSize
        elif self.isDown: dy = tileSize
        dx = dy / math.tan(self.rayAngle)
        
        while (nextIntersectionX <= screenX and nextIntersectionX >= 0 and nextIntersectionY <= screenY and nextIntersectionY >= 0):
            if self.map.isWall(nextIntersectionX, nextIntersectionY):
                isHorizontalWall = True
                horizontalHitX, horizontalHitY = nextIntersectionX, nextIntersectionY
                break
            else:
                nextIntersectionX += dx
                nextIntersectionY += dy
        
        isVerticalWall = False
        verticalHitX, verticalHitY = 0, 0
        
        if self.isLeft: firstIntersectionX = (self.player.x // tileSize) * tileSize - 1
        elif self.isRight: firstIntersectionX = (self.player.x // tileSize) * tileSize + tileSize
        
        firstIntersectionY = (firstIntersectionX - self.player.x) * math.tan(self.rayAngle) + self.player.y
        nextIntersectionX, nextIntersectionY = firstIntersectionX, firstIntersectionY
        dx, dy = 0, 0
        
        if self.isLeft: dx = -tileSize
        elif self.isRight: dx = tileSize
        dy = dx * math.tan(self.rayAngle)
        
        while (nextIntersectionX <= screenX and nextIntersectionX >= 0 and nextIntersectionY <= screenY and nextIntersectionY >= 0):
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
        else:
            self.wallHitX, self.wallHitY = verticalHitX, verticalHitY
        
        self.rayDistance = distanceBetweenPoints(self.player.x, self.player.y, self.wallHitX, self.wallHitY) * (math.cos(self.player.angle- self.rayAngle))
        
    def draw(self, display):
        pygame.draw.line(display, self.player.color, (self.player.x, self.player.y),(self.wallHitX, self.wallHitY)) 
        
class RayCaster:
    def __init__(self, player, map):
        self.rays = []
        self.player: Player = player
        self.map = map
        
    def castAll(self):
        self.rays: list[Ray] = []
        self.rayAngle = self.player.angle - (FOV / 2)
        for _ in range(rayNumber):
            ray = Ray(self.rayAngle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)
            self.rayAngle += FOV / rayNumber
            
    def drawAll(self, display):
        for i, ray in enumerate(self.rays):
            ray.draw(display)
            projectionHeight = (32) * ((screenX / 2) / (math.tan(FOV / 2))) / ray.rayDistance
            wallColor = (255 - min(255, ray.rayDistance * 0.5), 0, 0)
            pygame.draw.rect(display, wallColor, (i * resolution, (screenY // 2) - (projectionHeight // 2), resolution, projectionHeight))
            
        


rayMap = Map()
rayPlayer = Player(rayMap)
rayCaster = RayCaster(rayPlayer, rayMap)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    rayPlayer.update()
    rayCaster.castAll()    
    
    
    display.fill((0,0,0))
    rayMap.draw(display)
    rayPlayer.draw(display)
    rayCaster.drawAll(display)
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        resolution += 1
    if keys[pygame.K_DOWN]:
        resolution -= 1
        if resolution < 1: resolution = 1
    
    if keys[pygame.K_RIGHT]:
        FOV += 1 * (math.pi / 180)
        if FOV > 179 * (math.pi / 180): FOV = 179 * (math.pi / 180)
    if keys[pygame.K_LEFT]:
        FOV -= 1 * (math.pi / 180)
        if FOV < 1 * (math.pi / 180): FOV = 1 * (math.pi / 180)
    
    rayNumber = (screenX // resolution)
    pygame.display.set_caption(f"Raycaster - Resolution: {resolution} - Rays: {rayNumber} - FOV: {round(FOV * (180 / math.pi), 2)}")
    
    
            
    pygame.display.update()