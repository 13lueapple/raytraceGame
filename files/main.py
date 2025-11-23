import pygame, math, sys
import setting



display = pygame.display.set_mode((setting.screenX * 2, setting.screenY))
clock = pygame.time.Clock()

from rayMap import Map
from rayPlayer import Player
from rayCaster import RayCaster


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
    



    #setting adjustment
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        setting.resolution += 1
    if keys[pygame.K_DOWN]:
        setting.resolution -= 1
        if setting.resolution < 1: setting.resolution = 1
    
    if keys[pygame.K_RIGHT]:
        setting.FOV += 1 * (math.pi / 180)
        if setting.FOV > 179 * (math.pi / 180): setting.FOV = 179 * (math.pi / 180)
    if keys[pygame.K_LEFT]:
        setting.FOV -= 1 * (math.pi / 180)
        if setting.FOV < 1 * (math.pi / 180): setting.FOV = 1 * (math.pi / 180)
        
    if keys[pygame.K_LSHIFT]:
        rayPlayer.moveSpeed = 4
    else: rayPlayer.moveSpeed = 2
    
    setting.rayNumber = (setting.screenX // setting.resolution)
    pygame.display.set_caption(f"Raycaster - setting.resolution: {setting.resolution} - Rays: {setting.rayNumber} - setting.FOV: {round(setting.FOV * (180 / math.pi), 2)}")
    
    
            
    pygame.display.update()