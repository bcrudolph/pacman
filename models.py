#!/usr/bin/env python

import os, sys, glob
import pygame
from pygame.locals import *
import utils
import config

class Pacman(pygame.sprite.Sprite):
    """
    Pacman class.This is general character of the game
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        #number of eaten pacdots
        self.pac_dots = 0
        self.flash_dots = 0

        # current position
        self.x_pos = 0
        self.y_pos = 0 
        #one step is a 5 pixels
        self.x_step = 5
        self.y_step = 5
        
        #path to frames
        self.anim = glob.glob(config.pacman_dir+"/*.png")
        self.anim.sort()
        
        #animation speed
        #self.anim_speed_init = 5
        #self.anim_speed = self.anim_speed_init
        
        #animation position
        self.anim_num = 0
        self.anim_max  = len(self.anim)-1
        #download an image  
        self.image, self.rect = utils.load_image(self.anim[0], -1)

    def __anim_update(self):
            #self.anim_speed -= 1
            self.image, self.rect = utils.load_image(self.anim[self.anim_num], -1)
        #self.anim_speed = self.anim_speed_init
            if self.anim_num == self.anim_max:
                self.anim_num = 0
            else:
                self.anim_num += 1

    #TODO
    def __spin(self):
        center = self.rect.center

    def move(self, key):
        x_move = False
        y_move = False

        if key == K_RIGHT:
            self.x_pos += self.x_step
            self.__anim_update()
        elif key == K_LEFT:
            self.x_pos -= self.x_step
            self.__anim_update()
        elif key == K_UP:
            self.y_pos -= self.y_step 
            self.__anim_update()
        elif key == K_DOWN:
            self.y_pos += self.y_step
            self.__anim_update()

        self.rect.move_ip(self.x_pos, self.y_pos)

class PacDot(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(os.path.join(config.img_dir,"pac_dot.png"))
        if rect != None:
            self.rect = rect
