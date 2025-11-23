import math

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0: angle += (2 * math.pi)
    return angle


def distanceBetweenPoints(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)