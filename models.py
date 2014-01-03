#!/usr/bin/env python

import os, sys, glob
import pygame
import random
from pygame.locals import *

import utils
import config


class BasicSprite(pygame.sprite.Sprite):
    """
    Basic sprite class for all models
    """
    def __init__(self, center_point, image_path, colorkey = None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image_path, colorkey)
        self.rect.center = center_point


#inheritance from pygame.sprite.Sprite cause pacman is an animation
class Pacman(pygame.sprite.Sprite):
    """
    Pacman class.This is general character of the game
    """

    def __init__(self, center_point, frame_list_path):
        pygame.sprite.Sprite.__init__(self)

        #path to frames
        self.anim = glob.glob(frame_list_path)
        self.anim.sort()

        #animation position
        self.anim_num = 0
        self.anim_max = len(self.anim)-1

        #download an image
        self.image, self.rect = utils.load_image(self.anim[0], -1)
        self.rect.center = center_point

        #number of eaten pellets
        self.pellets = 0
        self.score = 0
        #each time step
        self.step = 4
        self.x_step = 0
        self.y_step = 0

        self.dir = 0
        self.x_dir = [0, self.step, -self.step, 0, 0]
        self.y_dir = [0, 0, 0, -self.step, self.step]

    def __anim_update(self):
        self.image, self.rect = utils.load_image(self.anim[self.anim_num], -1)
        if self.anim_num == self.anim_max:
            self.anim_num = 0
        else:
            self.anim_num += 1

    #TODO
    def __spin(self):
        center = self.rect.center
    def __step(self, dir):
        self.x_step = self.x_dir[dir]
        self.y_step = self.y_dir[dir]

        #self.rect.x += self.x_step
        #self.rect.y += self.y_step
        self.rect.move_ip(self.x_step, self.y_step)

    def move(self, blocks, key):

        if key == K_RIGHT:
            self.dir = 1
           # self.__anim_update()
        elif key == K_LEFT:
            self.dir = 2
            #self.__anim_update()
        elif key == K_UP:
            self.dir = 3
            #self.__anim_update()
        elif key == K_DOWN:
            self.dir = 4
            #self.__anim_update()

        self.__step(self.dir)

        if pygame.sprite.spritecollide(self, blocks, False):
            self.rect.x -= self.x_step
            self.rect.y -= self.y_step
            self.step = 0
            self.dir = 0

class Enemy(BasicSprite):
    '''
    Enemy class for blinky, pinky, clyde, inky
    '''

    def __init__(self, center_point, image_path, colorkey = None):
        super(Enemy, self).__init__(center_point, image_path, colorkey)

        self.image, self.rect = utils.load_image(image_path, colorkey)
        self.rect.center = center_point

        self.step = 2

        self.x_move = 0
        self.y_move = 0

        self.dir = 1
        self.next_dir = 3
        self.x_dir = [0, self.step, -self.step, 0, 0]
        self.y_dir = [0, 0, 0, -self.step, self.step]

    def __step(self, dir):
        self.x_move = self.x_dir[dir]
        self.y_move = self.y_dir[dir]

    ##magic for ghosts strategy
    def move(self, blocks):
        self.__step(self.next_dir)
        self.rect.move_ip(self.x_move, self.y_move)

        if pygame.sprite.spritecollide(self, blocks, False):
            self.rect.move_ip(-self.x_move,-self.y_move)
            self.__step(self.dir)
            self.rect.move_ip(self.x_move, self.y_move)

            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.move_ip(-self.x_move,-self.y_move)
                if self.next_dir < 3:
                    self.next_dir = random.randint(3,4)
                else:
                    self.next_dir = random.randint(1,2)
        else:
            self.dir = self.next_dir
            if self.next_dir < 3:
                self.next_dir = random.randint(3,4)
            else:
                self.next_dir = random.randint(1,2)



