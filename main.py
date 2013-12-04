"""
    My test for 2D platformer movement.
    Here we have collision detection, smooth accelerated movement,
    seperate world and window coordinates, and camera movement.
"""

import pygame
from pygame.locals import *
pygame.init()

import sys
import time

from lib import (entities, camera, draw, level, hud, tmx)

# font for drawing congrats at the end
# placing it here cause its 1AM and I'm too sleepy to care
WHITE     =  (255, 255, 255)
LIGHTBLUE =  (128, 128, 255)
MAINFONT = pygame.font.SysFont("Courier New", 100)
BACKFONT = pygame.font.SysFont("Courier New", 102)
class main():
    def __init__(self):
        self.level = 1

    # Screen Constants
    FPS = 60
    FPS_limit = True
    WINDOWWIDTH = 800
    WINDOWHEIGHT = 600
    FLAGS = HWSURFACE | DOUBLEBUF
    showText = False
    
    def play_game(self):
        # Set up screen
        self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), self.FLAGS)
        pygame.display.set_caption('2D Platforming Test')
        self.clock = pygame.time.Clock()
        
        # Set up objects
        self.tilemap = tmx.load('level_1.tmx', self.screen.get_size())
        self.currentLevel = level.Level("levels/level_1.lvl")

        # the second line will spawn the player at the end of the level. Useful for debugging
        self.player = entities.Player(self.currentLevel, (4, 56, 60, 90))
        #self.player = entities.Player(self.currentLevel, (90, 2, 60, 90))
        self.tilemap.set_focus(self.player.rect.centerx, self.player.rect.centery)

        # original speed settings for 30 FPS
        #
        #if self.FPS == 30:
        #    self.player.maxSpeed = 16
        #    self.player.accel_amt = 3
        #    self.player.airaccel_amt = 2
        #    self.player.deaccel_amt = 10
        #    self.player.fallAccel = 4
        #    self.animation_speed = 0.015
        #
        self.cameraObj = camera.Camera(self.player.rect, 
                                       self.WINDOWWIDTH, 
                                       self.WINDOWHEIGHT)
        self.OSD_text = hud.OSD()
        #dt = 0
        # Game loop
        while True:
            self.keys = self.collect_input()
            level_over = self.player.update(self.keys, self.currentLevel)

            # a very hackish way to change levels. So sue me.
            if level_over and self.level == 1:
                self.level = 2
                self.tilemap.set_focus(self.player.rect.centerx, self.player.rect.centery)
                self.tilemap = tmx.load('level_2.tmx', self.screen.get_size())
                self.currentLevel = level.Level("levels/level_2.lvl")

                # the second line will spawn the player at the end. Useful for debugging
                self.player = entities.Player(self.currentLevel, (3, 3, 60, 90))
                #self.player = entities.Player(self.currentLevel, (116, 8, 60, 90))
                self.cameraObj = camera.Camera(self.player.rect,
                                       self.WINDOWWIDTH,
                                       self.WINDOWHEIGHT)
                continue
            elif level_over and self.level == 2:
                # display congrats. This is a terrible place to put this code.
                textobj = MAINFONT.render("YOU WIN!", 1, WHITE)
                backtext = BACKFONT.render("YOU WIN!", 1, LIGHTBLUE)
                textrect = textobj.get_rect()
                textrect.topleft = (self.WINDOWWIDTH/2 - textrect.width/2, self.WINDOWHEIGHT/2 - textrect.height/2)
                backtextrect = backtext.get_rect()
                backtextrect.topleft = (self.WINDOWWIDTH/2 - backtextrect.width/2, self.WINDOWHEIGHT/2 - backtextrect.height/2)
                self.screen.blit(textobj, textrect)
                self.screen.blit(backtext, backtextrect)
                pygame.display.update()
                # spin wait while waiting for the user to close the game
                while True:
                    #pygame.time.wait(100)
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()
                            sys.exit()
            self.cameraObj.update(self.player.cameraRect, self.currentLevel)
            self.OSD_text.update(self)

            self.tilemap.set_focus(self.player.rect.centerx, self.player.rect.centery)
            # Fill the screen with an R,G,B color to erase the previous drawings
            self.screen.fill((0, 0, 0))
            #draw the backgrounds, charater and then the blocks in that order
            self.tilemap.layers[0].draw(self.screen)
            self.tilemap.layers[1].draw(self.screen)
            self.tilemap.layers[2].draw(self.screen)
            draw.draw_entities(self.screen, (self.player,), self.cameraObj)
            self.tilemap.layers[3].draw(self.screen)
            # uncomment to debug the level collision map
            #draw.draw_level(self.screen, self.currentLevel, self.cameraObj)
            # Refresh the display window.
            pygame.display.flip()
            #if self.showText:
            #    draw.draw_OSD(self.screen, self.OSD_text.text)
            pygame.display.update()
            self.clock.tick(self.FPS)
            
    def collect_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                #if event.key == K_x:
                #    self.showText = not self.showText
                # repurposed the 'z' key to frame limit to 30 fps
                #if event.key == K_z:
                #    #self.level_draw = not self.level_draw
                #    #if self.FPS > 30:
                #    #    self.FPS = 30
                #    #else:
                #    #    self.FPS = 60
                pass

        keys = pygame.key.get_pressed()
        return keys

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main().play_game()')
    main().play_game()
