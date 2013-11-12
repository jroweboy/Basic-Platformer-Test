import pygame
from level import *

class Camera(pygame.Rect):
    # removed the camera slack because it was hard to move the background if it was there
    cameraSlackX = 0
    cameraSlackY = 0
    def __init__(self, targetRect, windowWidth, windowHeight):
        super(Camera,self).__init__(targetRect.centerx-(windowWidth/2), 
                                    targetRect.centery-(windowHeight/2), 
                                    windowWidth, windowHeight)
        
    def update(self, rect, level):
        # Figure out if rect has exceeded camera slack
        if self.centerx - rect.centerx > self.cameraSlackX:
            self.left = rect.centerx + self.cameraSlackX - self.width/2
        elif rect.centerx - self.centerx > self.cameraSlackX:
            self.left = rect.centerx - self.cameraSlackX - self.width/2
        if self.centery - rect.centery > self.cameraSlackY:
            self.top = rect.centery + self.cameraSlackY - self.height/2
        elif rect.centery - self.centery > self.cameraSlackY:
            self.top = rect.centery - self.cameraSlackY - self.height/2
        
        # This keeps the camera within the boundaries of the level
        if self.right > level.rightEdge:
            self.right = level.rightEdge
        elif self.left < 0:
            self.left = 0
        if self.top < 0:
            self.top = 0
        elif self.bottom > level.bottomEdge:
            self.bottom = level.bottomEdge
        
        return self