import pygame
import time
import random
import math;
pygame.font.init()

#------------  R    G    B  ----------------
WHITE     =  (255, 255, 255)
GREY      =  (128, 128, 128)
BLACK     =  (  0,   0,   0)
RED       =  (255,   0,   0)
GREEN     =  (  0, 255,   0)
BLUE      =  (  0,   0, 255)
HOTPINK   =  (255, 110, 168)   
LIGHTBLUE =  (128, 128, 255)

BLOCK_COLOR = WHITE
PLAYER_COLOR = HOTPINK
BACKGROUND_COLOR = BLACK
OSD_COLOR = GREY

FONTSIZE = 20
MAINFONT = pygame.font.SysFont("Courier New", FONTSIZE)
#BACKGROUND = pygame.transform.scale(pygame.image.load("lib\\background.jpg"), (800, 600))


def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_OSD(surface, strings):
    pos = 0
    for text in strings:
        drawText(text, MAINFONT, OSD_COLOR, surface, 10, pos)
        pos += FONTSIZE

def draw_level(surface, level, camera):
    '''
    When using a TMX draw level is not used. It IS still used for debugging the collision bounds though
    '''
    #surface.blit(BACKGROUND, (0, 0))
    #surface.fill(BACKGROUND_COLOR)
    # change the render code to only draw blocks that are near the camera
    #x, y = int(camera.x / level.blockWidth) - 1, int(camera.y / level.blockHeight) - 1
    #x2, y2 = x + math.ceil(800 / level.blockWidth), math.ceil(600 / level.blockHeight)
    #
    #for a in range(x, x2+1):
    #    for b in range(y, y2+1):
    #        #blockRect = pygame.Rect(a*level.blockWidth, b*level.blockHeight, level.blockWidth, level.blockHeight)
    #        block = level.tmx.getTileImage(a,b,level)
    #        surface.blit(block,)

    # Rendering involves a little conversion of level coordinates to surface coordinates
    # The active area makes sure only blocks that are shown on screen are rendered
    for y in range(level.levelHeight):
        for x in range(level.levelWidth):
            blockRect = pygame.Rect(x*level.blockWidth, y*level.blockHeight, level.blockWidth, level.blockWidth)
            if camera.colliderect(blockRect):
                if level.collisionLayer[y][x] == level.blank:
                    continue
                if level.collisionLayer[y][x] == level.block:
                    surface.blit(level.blockSurf,
                                 ((x*level.blockWidth) - camera.left,
                                 (y*level.blockHeight) - camera.top,))
                    #pygame.draw.rect(surface, BLOCK_COLOR,
                    #((x*level.blockWidth) - camera.left,
                     #(y*level.blockHeight) - camera.top,
                     #level.blockWidth,
                     #level.blockHeight))


# This function is needed to draw a rect within the camera
from lib.entities import Player
def draw_entities(surface, sprites, camera):
    for sprite in sprites:
        # warning : I wanted to increase the player sprites size without affecting the
        # bounding box so I ended up hacking it into the draw routine right here.
        # TODO: write this better
        if type(sprite) is Player:
            surface.blit(sprite.image, (sprite.rect.left - camera.left,
                                    sprite.rect.top - 20 - camera.top))
        else:
            surface.blit(sprite.image, (sprite.rect.left - camera.left,
                                    sprite.rect.top - camera.top))