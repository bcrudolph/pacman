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
    Pacman class.This is the main character of the game
    """

    def __init__(self, center_point, frame_list_path):
        pygame.sprite.Sprite.__init__(self)

        #path to frames
        self.anim = glob.glob(frame_list_path)
        self.anim.sort()
        self.anim_horizontal = self.anim[:4]
        self.anim_vertical = self.anim[4:]

        #maximum number of frames
        self.anim_max = len(self.anim[:4])-1
        self.anim_num_h = 0
        self.anim_num_v = 0

        #download an image
        self.image, self.rect = utils.load_image(self.anim[0], -1)
        self.rect.center = center_point

        #number of eaten pellets
        self.pellets = 0
        self.score = 0
        #each time step
        self.step = 4
        self.x_dir = [0, self.step, -self.step, 0, 0]
        self.y_dir = [0, 0, 0, -self.step, self.step]

    def __anim_update_h(self):
        self.image = pygame.image.load(self.anim_horizontal[self.anim_num_h])
        if self.anim_num_h == self.anim_max:
            self.anim_num_h = 0
        else:
            self.anim_num_h += 1

    def __anim_update_v(self):
        self.image = pygame.image.load(self.anim_vertical[self.anim_num_v])
        if self.anim_num_v == self.anim_max:
            self.anim_num_v = 0
        else:
            self.anim_num_v += 1

    def __spin(self, key):
        if key == K_LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
        if key == K_UP:
            self.image = pygame.transform.flip(self.image, 0, 1)

        center = self.rect.center

    def __change_dir(self, dir):
        return self.x_dir[dir], self.y_dir[dir]

    def __step_front(self, *args):
        self.rect.x += args[0]
        self.rect.y += args[1]

    def __step_back(self, *args):
        self.rect.x -= args[0]
        self.rect.y -= args[1]

    def move(self, blocks, key):
        direction = 0
        if key == K_RIGHT:
            direction = 1
            self.__anim_update_h()
        elif key == K_LEFT:
            direction = 2
            self.__anim_update_h()
            self.__spin(key)
        elif key == K_UP:
            direction = 3
            self.__anim_update_v()
            self.__spin(key)
        elif key == K_DOWN:
            direction = 4
            self.__anim_update_v()

        x_step, y_step = self.__change_dir(direction)
        self.__step_front(x_step, y_step)

        if pygame.sprite.spritecollide(self, blocks, False):
            self.__step_back(x_step, y_step)
            self.step = 0

class Enemy(BasicSprite):
    '''
    Enemy class for blinky, pinky, clyde, inky
    '''

    def __init__(self, center_point, image_path, colorkey = None):
        super(Enemy, self).__init__(center_point, image_path, colorkey)

        self.image, self.rect = utils.load_image(image_path, colorkey)
        self.rect.center = center_point

        self.step = 2

        #initial values for direction
        self.dir = 1
        self.next_dir = 3

        self.x_dir = [0, self.step, -self.step, 0, 0]
        self.y_dir = [0, 0, 0, -self.step, self.step]

    def __step(self, dir):
        return self.x_dir[dir], self.y_dir[dir]

    ##magic for ghosts strategy
    def move(self, blocks):
        x_move, y_move = self.__step(self.next_dir)
        self.rect.move_ip(x_move, y_move)

        if pygame.sprite.spritecollide(self, blocks, False):
            self.rect.move_ip(-x_move, -y_move)
            x_move, y_move = self.__step(self.dir)
            self.rect.move_ip(x_move, y_move)

            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.move_ip(-x_move, -y_move)
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
