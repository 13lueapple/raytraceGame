import math

tileSize = 32
screenX = tileSize * 20
screenY = tileSize * 15


FOV = 60 * (math.pi / 180)
resolution = 4
rayNumber = (screenX // resolution)
