#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import models
import config

class Game:
    def __init__(self,
                 width = config.screen_width,
                 height = config.screen_height):
        # initialization all pygame modules
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman")
        pygame.mouse.set_visible(0)
        #set repetition  (set_repeat(after first keydown, after any other))
        pygame.key.set_repeat(30,30)

    def __load_wall_sprites(self):
        y_offset = 40
        x_offset = 70
        wall_width = 20
        wall_divider = 7
        wall_coords = [(x_offset,
                        y_offset,
                        self.width-2*x_offset,
                        wall_width), #top

                        (x_offset,
                        self.height-y_offset-wall_width,
                        self.width-2*x_offset,
                        wall_width), #bottom

                        (x_offset,
                        y_offset+wall_width,
                        wall_width,
                        (self.height - 2*y_offset-wall_width)/2 -config.portal_width), #left top

                        (x_offset,
                         y_offset+(self.height-2*y_offset-wall_width)/2+config.portal_width,
                         wall_width,
                         (self.height - 2*y_offset-wall_width)/2 -config.portal_width), #left bottom

                        (self.width-x_offset-wall_width,
                         y_offset+wall_width,
                         wall_width,
                         (self.height - 2*y_offset-wall_width)/2 -config.portal_width), #right top

                        (self.width-x_offset-wall_width,
                         y_offset+(self.height-2*y_offset-wall_width)/2+config.portal_width,
                         wall_width,
                         (self.height - 2*y_offset-wall_width)/2 -config.portal_width), #right bottom

                        (x_offset+wall_width+config.aisle_width,
                         y_offset+wall_width+config.aisle_height,
                         (self.width-2*x_offset)/wall_divider,
                         wall_width), #1 undertop line block

                        (x_offset+wall_width+2*config.aisle_width+(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width+config.aisle_height,
                         (self.width-2*x_offset)/wall_divider,
                         wall_width), #2 undertop line block

                        (x_offset+wall_width+3*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width,
                         wall_width,
                         (self.width-2*x_offset)/wall_divider), #center undertop column block

                        (x_offset+2*wall_width+4*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width+config.aisle_height,
                         (self.width-2*x_offset)/wall_divider,
                         wall_width), #3 undertop line block

                        (x_offset+2*wall_width+5*config.aisle_width+3*(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width+config.aisle_height,
                         (self.width-2*x_offset)/wall_divider,
                         wall_width), #4 undertop line block

                        (x_offset+wall_width+2*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width+config.aisle_width+(self.width-2*x_offset)/wall_divider,
                         (self.width-2*x_offset)/wall_divider,
                        wall_width), #center line block 1(horizontal part)

                        (x_offset+wall_width+3*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+wall_width+(self.width-2*x_offset)/wall_divider+config.aisle_width+wall_width,
                         wall_width,
                         ((self.width-2*x_offset)/wall_divider)/3), #center column block 1(vertical part)

                        (x_offset+wall_width+2*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+3*wall_width+3*config.aisle_width+4*(self.width-2*x_offset)/wall_divider/3,
                         (self.width-2*x_offset)/wall_divider,
                        wall_width), #center line block 2(horizontal part)

                        (x_offset+wall_width+3*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         y_offset+4*wall_width+4*(self.width-2*x_offset)/wall_divider/3+3*config.aisle_width,
                         wall_width,
                         ((self.width-2*x_offset)/wall_divider)/3), #center column block 2(vertical part)

                        (x_offset+wall_width+2*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                        y_offset+4*wall_width+4*config.aisle_width+5*(self.width-2*x_offset)/wall_divider/3,
                        (self.width-2*x_offset)/wall_divider,
                        wall_width), #center line block 3(horizontal part)

                        (x_offset+wall_width+3*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                        y_offset+5*wall_width+5*(self.width-2*x_offset)/wall_divider/3+4*config.aisle_width,
                        wall_width,
                        ((self.width-2*x_offset)/wall_divider)/3), #center column block 3(vertical part)

                        (x_offset+wall_width+config.aisle_width,
                         y_offset+9*wall_width/2+5*(self.width-2*x_offset)/wall_divider/3+2*config.aisle_width,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #1 under portal line block

                        (x_offset+2*config.aisle_width+(self.width-2*x_offset)/wall_divider,
                         y_offset+9*wall_width/2+5*(self.width-2*x_offset)/wall_divider/3+2*config.aisle_width,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #2 under portal line block

                        (x_offset+3*wall_width+4*config.aisle_width+3*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider,
                         y_offset+9*wall_width/2+5*(self.width-2*x_offset)/wall_divider/3+2*config.aisle_width,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #3 under portal line block

                        (x_offset+2*wall_width+5*config.aisle_width+4*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider,
                         y_offset+9*wall_width/2+5*(self.width-2*x_offset)/wall_divider/3+2*config.aisle_width,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #4 under portal line block

                        (x_offset+2*config.aisle_width+(self.width-2*x_offset)/wall_divider+wall_width,
                         y_offset+wall_width+5*(self.width-2*x_offset)/wall_divider/3,
                         (self.width-4*x_offset)/wall_divider - wall_width,
                         wall_width), #horizontal part of left vertical T - block

                        (x_offset+3*wall_width+4*config.aisle_width+2*(self.width-2*x_offset)/wall_divider+(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider,
                         y_offset+wall_width+5*(self.width-2*x_offset)/wall_divider/3,
                         (self.width-4*x_offset)/wall_divider - wall_width,
                         wall_width), #horizontal part of right vertical T - block

                        (x_offset+2*config.aisle_width+(self.width-2*x_offset)/wall_divider,
                        y_offset+wall_width+4*(self.width-2*x_offset)/wall_divider/3,
                        wall_width,
                        (self.width-2*x_offset)/wall_divider), #vertical part of right vertical T -block

                        (x_offset+2*wall_width+4*config.aisle_width+3*(self.width-2*x_offset)/wall_divider-1,
                        y_offset+wall_width+4*(self.width-2*x_offset)/wall_divider/3,
                        wall_width,
                        (self.width-2*x_offset)/wall_divider), #vertical part of left vertical T -block

                        (x_offset+wall_width+config.aisle_width,
                         y_offset+4*wall_width+(self.width-2*x_offset)/wall_divider/2,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #1 under first line left block

                        (x_offset+2*wall_width+5*config.aisle_width+4*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider,
                         y_offset+4*wall_width+(self.width-2*x_offset)/wall_divider/2,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), #2 under first line right block

                         (x_offset+wall_width,
                         y_offset+13*wall_width/2+(self.width-2*x_offset)/wall_divider/2,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), # top left portal block

                        (x_offset+2*wall_width+6*config.aisle_width+4*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider+wall_width/2,
                         y_offset+13*wall_width/2+(self.width-2*x_offset)/wall_divider/2,
                         (self.width-4*x_offset)/wall_divider,
                         wall_width), # top right right block

                        (x_offset+wall_width,
                         y_offset+13*wall_width/2+(self.width-2*x_offset)/wall_divider/2+2*config.portal_width,
                         2*(self.width-2*x_offset)/wall_divider-wall_width/2,
                         wall_width), # bottom left portal block

                        (x_offset+wall_width+6*config.aisle_width+3*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider+wall_width/2,
                         y_offset+13*wall_width/2+(self.width-2*x_offset)/wall_divider/2+2*config.portal_width,
                         (self.width-4*x_offset)/wall_divider+wall_width+(self.width-2*x_offset)/wall_divider+wall_width/2,
                         wall_width), # bottom right right block

                        (x_offset+wall_width+config.aisle_width,
                         y_offset+13*wall_width/2+2*(self.width-2*x_offset)/wall_divider+2*config.aisle_width,
                         2*(self.width-4*x_offset)/wall_divider+config.aisle_width,
                         wall_width), #left under bottom line block

                        (x_offset+3*wall_width+4*config.aisle_width+3*(self.width-2*x_offset)/wall_divider-(self.width-4*x_offset)/wall_divider,
                         y_offset+13*wall_width/2+2*(self.width-2*x_offset)/wall_divider+2*config.aisle_width,
                         2*(self.width-4*x_offset)/wall_divider+config.aisle_width,
                         wall_width), #right under bottom line block

                        (x_offset+wall_width+2*config.aisle_width+(self.width-4*x_offset)/wall_divider,
                        y_offset+4*wall_width+5*(self.width-2*x_offset)/wall_divider/3+4*config.aisle_width,
                        wall_width,
                        ((self.width-2*x_offset)/wall_divider)/3), #vertical block for under bottom right line

                        (x_offset+wall_width+2*config.aisle_width+4*(self.width-2*x_offset)/wall_divider,
                        y_offset+4*wall_width+5*(self.width-2*x_offset)/wall_divider/3+4*config.aisle_width,
                        wall_width,
                        ((self.width-2*x_offset)/wall_divider)/3), #vertical block for under bottom left line

                        (x_offset+wall_width+config.aisle_width,
                        y_offset+3*wall_width+5*(self.width-2*x_offset)/wall_divider/3+4*config.aisle_width,
                        wall_width,
                        ((self.width-2*x_offset)/wall_divider)/3), #vertical right block for under portal line blocks

                        (x_offset+wall_width+3*config.aisle_width+4*(self.width-2*x_offset)/wall_divider+(self.width-4*x_offset)/wall_divider-1,
                        y_offset+3*wall_width+5*(self.width-2*x_offset)/wall_divider/3+4*config.aisle_width,
                        wall_width,
                        ((self.width-2*x_offset)/wall_divider)/3) #vertical left block for under portal line blocks

                        ## enemy center box

                        #(x_offset+wall_width+2*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         #y_offset+4*wall_width+config.aisle_width+(self.width-2*x_offset)/wall_divider,
                         #(self.width-2*x_offset)/wall_divider,
                        #wall_width/3), #top line

                         #(x_offset+wall_width+2*config.aisle_width+2*(self.width-2*x_offset)/wall_divider,
                         #y_offset+11*wall_width/2-1+config.aisle_width+(self.width-2*x_offset)/wall_divider,
                         #(self.width-2*x_offset)/wall_divider,
                        #wall_width/3), #top line

                    ]

        self.wall_sprites = pygame.sprite.Group()

        for coords in wall_coords:
            self.wall_sprites.add(models.Wall(coords[0], coords[1], coords[2], coords[3]))

    def __load_pac_dots(self):
        #initialize sprites group 
        self.pacdots_sprites = pygame.sprite.Group()
        
        #accordingly screen resolution, filling it with plain pac-dots(pac_dot.png (3x3))
        for x in range(4,int(self.width)/20-3):
            for y in range(4,int(self.height)/20-3):
                self.pacdots_sprites.add(models.PacDot(pygame.Rect(x*20, y*20, 3, 3)))

    def __load_sprites(self):
        #getting pacman character sprite
        self.pacman = models.Pacman(50+3*config.aisle_width+2*(self.width-80)/6,
                                     self.height/2+(self.width-150)/6)
        self.pacman_sprite = pygame.sprite.RenderPlain((self.pacman))
        
        #getting enemies characters sprites
        self.blinky = models.Enemy("blinky.png", self.width/2, self.height/2)
        self.blinky_sprite = pygame.sprite.RenderPlain((self.blinky))

        self.pinky = models.Enemy("pinky.png", self.width/2, self.height/2+15)
        self.pinky_sprite = pygame.sprite.RenderPlain((self.pinky))

        self.inky = models.Enemy("inky.png", self.width/2, self.height/2+30)
        self.inky_sprite = pygame.sprite.RenderPlain((self.inky))

        self.clyde = models.Enemy("clyde.png", self.width/2, self.height/2+45)
        self.clyde_sprite = pygame.sprite.RenderPlain((self.clyde))
    
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
        #loading wall sprites
        self.__load_wall_sprites()
        #loading pac dots
        self.__load_pac_dots()
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
                                self.pacman.move(self.wall_sprites,event.key)
            
            # enemies random move
            self.blinky.move(self.wall_sprites)
            self.inky.move(self.wall_sprites)
            self.clyde.move(self.wall_sprites)
            self.pinky.move(self.wall_sprites)

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
            self.wall_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
            self.blinky_sprite.draw(self.screen)
            self.pinky_sprite.draw(self.screen)
            self.inky_sprite.draw(self.screen)
            self.clyde_sprite.draw(self.screen)
            pygame.display.flip()
                    






