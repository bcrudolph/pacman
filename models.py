#!/usr/bin/env python

import os, sys, glob
import pygame
import random
from pygame.locals import *

import utils
import config

class Pacman(pygame.sprite.Sprite):
    """
    Pacman class.This is general character of the game
    """
    def __init__(self, init_x = 0,init_y = 0):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        
        #number of eaten pacdots
        self.pac_dots = 0
        self.flash_dots = 0

        #one step is a 5 pixels
        self.x_step = init_x
        self.y_step = init_y
        
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
        self.rect.topleft = init_x, init_y

    def __anim_update(self):
            #self.anim_speed -= 1
            self.image, self.rect = utils.load_image(self.anim[self.anim_num], -1)
        #self.anim_speed = self.anim_speed_init
            if self.anim_num == self.anim_max:
                self.anim_num = 0
            else:
                self.anim_num += 1

    def __walk(self, x_s, y_s):
        self.x_step += x_s
        self.y_step += y_s
    #TODO
    def __spin(self):
        center = self.rect.center

    def move(self,walls, key):
        if key == K_RIGHT:
            self.__walk(5,0)
            self.__anim_update()
        elif key == K_LEFT:
            self.__walk(-5,0)
            self.__anim_update()
        elif key == K_UP:
            self.__walk(0,-5)
            self.__anim_update()
        elif key == K_DOWN:
            self.__walk(0, 5)
            self.__anim_update()

        self.rect.x += self.x_step

        blocks_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in blocks_hit:
            if self.x_step < 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.y_step

        blocks_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in blocks_hit:
            if self.y_step < 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class PacDot(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(os.path.join(config.img_dir,"pac_dot.png"))
        if rect != None:
            self.rect = rect

class Enemy(pygame.sprite.Sprite):
    '''
    Enemies class for blinky, pinky, clyde, inky
    '''
    def __init__(self, pathname, init_pos_x = 0, init_pos_y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(os.path.join(config.enemy_dir, pathname),-1)

        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.scr_width = self.screen.get_width()
        self.scr_height = self.screen.get_height()

        self.rect.topleft = init_pos_x, init_pos_y

        self.x_step = 2
        self.y_step = 2

    def __serve(self):
        angle = random.randint(-45,45)


    def move(self, walls):
        self.rect.x += self.x_step

        blocks_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in blocks_hit:
            if self.rect.left < block.rect.left:
                self.rect.right = block.rect.left
                self.x_step=-self.x_step
            elif self.rect.right > block.rect.right:
                self.rect.left = block.rect.right
                self.x_step=-self.x_step

        self.rect.y += self.y_step

        blocks_hit = pygame.sprite.spritecollide(self, walls, False)
        for block in blocks_hit:
            if self.rect.top < block.rect.top:
                self.rect.bottom = block.rect.top
                self.y_step=-self.y_step
            elif self.rect.bottom > block.rect.bottom:
                self.rect.top = block.rect.bottom
                self.y_step=-self.y_step


class Wall(pygame.sprite.Sprite):
    def __init__(self,x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        #fill image with blue color
        self.image.fill((0,0,255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

