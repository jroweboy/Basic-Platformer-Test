import pygame


class Level(object):
    blank = '.'
    block = 'b'
    enemy = '^'
    exit = 'X'

    blockWidth = 75
    blockHeight = 75
    
    def __init__(self, level_data_filename):
        import re
        with open(level_data_filename, 'r') as f:
            self.levelRaw = f.readlines()
        # replace any of the visual blocks with just a regular block only for the collision layer
        self.collisionLayer = [re.sub("0", "b", row.strip('\n')) for row in self.levelRaw]

        self.levelWidth = len(self.collisionLayer[0])
        self.levelHeight = len(self.collisionLayer)
        
        self.leftEdge = 0
        self.topEdge = 0
        self.rightEdge = self.levelWidth * self.blockWidth
        self.bottomEdge = self.levelHeight * self.blockHeight
        
        
        self.blockSurf = pygame.Surface((self.blockWidth, self.blockHeight))
        self.blockSurf.fill((255,255,255))
        self.blockSurf.set_alpha(100)