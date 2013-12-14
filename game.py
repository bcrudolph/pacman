#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import models
import config

class Game:
    def __init__(self, width = 640, height = 480):
        # initialization all pygame modules
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman")
        pygame.mouse.set_visible(0)
        #set repetition  (set_repeat(after first keydown, after any other))
        pygame.key.set_repeat(30,30)

    def __load_sprites(self):
        #getting pacman character sprite
        self.pacman = models.Pacman()
        self.pacman_sprite = pygame.sprite.RenderPlain((self.pacman))
        
        #initialize sprites group 
        self.pacdots_sprites = pygame.sprite.Group()
        
        #accordingly screen resolution, filling it with plain pac-dots(pac_dot.png (3x3))
        for x in range(1,int(self.width/15)):
            for y in range(1,int(self.height/15)):
                self.pacdots_sprites.add(models.PacDot(pygame.Rect(x*15, y*15, 3, 3)))
    
    def __set_backgrnd(self):
        # add background on the screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


    def main_loop(self):
        #getting clock to control frame rate
        self.clock = pygame.time.Clock()
        
        #loading sprites
        self.__load_sprites()
        #setting background
        self.__set_backgrnd()

        while True:
            #60 FPS
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type is KEYDOWN:
                    if event.key == K_RIGHT \
                            or event.key == K_LEFT \
                            or event.key == K_UP \
                            or event.key == K_DOWN:
                                self.pacman.move(event.key)
                                
            #check collisions True means: kill sprite from group in collision
            pacman_dots_cols = pygame.sprite.spritecollide(self.pacman,
                                                            self.pacdots_sprites,
                                                            True)
            #count score 
            for dot in pacman_dots_cols:
                self.pacman.pac_dots += 1

            #adding background on the screen
            self.screen.blit(self.background, (0, 0))
            
            #draw sprites
            self.pacdots_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
            pygame.display.flip()
                    






