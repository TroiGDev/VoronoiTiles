import pygame

import pygame.surfarray as surfarray
import numpy as np

import math
import random

import pyRecorder

#initialize pygame window
pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('VoronoiTiles')

pyrecorder = pyRecorder.Recorder()

#CLASS DEFINITION -----------------------------------------------------------------------------------------------------------------------------------------

class voronoiPoint():
    def __init__(self, x, y, color):
        voronoiPoints.append(self)
        self.x = x
        self.y = y

        self.color = color              #color of drawn point

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 6)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 7, 3)

#FUNCTION DEFINITION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def voronoi_shader(x, y, r, g, b):
    #get closest voronoi point
    closestPoint = None
    closestDistance = math.inf
    for point in voronoiPoints:
        #get dist to current
        vecToPoint = (point.x - x, point.y - y)
        d = math.sqrt(vecToPoint[0]**2 + vecToPoint[1]**2)

        if d < closestDistance:
            closestDistance = d
            closestPoint = point

    if closestPoint == None:
        return [r, g, b]
    else:
        return [closestPoint.color[0], closestPoint.color[1], closestPoint.color[2]]
    
def voronoi_manhattan_shader(x, y, r, g, b):
    #get closest voronoi point
    closestPoint = None
    closestDistance = math.inf
    for point in voronoiPoints:
        #get dist to current
        vecToPoint = (point.x - x, point.y - y)
        d = abs(vecToPoint[0]) + abs(vecToPoint[1])

        if d < closestDistance:
            closestDistance = d
            closestPoint = point

    if closestPoint == None:
        return [r, g, b]
    else:
        return [closestPoint.color[0], closestPoint.color[1], closestPoint.color[2]]

#VARIABLE INITIALIZATION ----------------------------------------------------------------------------------------------------------------------------------------- 

voronoiPoints = []

def recalculateVoronoi():
    # create a numpy surfarray
    array = surfarray.pixels3d(screen)
    width, height = screen.get_size()

    #apply the shader calculations for each pixel
    for x in range(width):
        for y in range(height):
            r, g, b = array[x][y]

            #array[x][y] = voronoi_shader(x, y, r, g, b)
            array[x][y] = voronoi_manhattan_shader(x, y, r, g, b)

    #"unlock" the surface
    del array

for i in range(20):
    c = random.randint(50, 200)
    newPoint = voronoiPoint(random.randint(0, screenWidth), random.randint(0, screenHeight), (c, c, c))

c = random.randint(50, 200)
vPoint = voronoiPoint(0, screenHeight/2, (c, c, c))

#WHILE LOOP - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

t = 0

running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t += 1

    vPoint.x = screenWidth/300 * t

    recalculateVoronoi()

    #for point in voronoiPoints:
    #    point.draw()

    pyrecorder.takeShot(screen, t)
    pygame.display.flip()

    if t == 300:
        running = False

pyrecorder.compileToVideo(60)

# Quit Pygame
pygame.quit()
