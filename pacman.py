#!/usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
import utils

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 300
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Pacman") 

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0,0,0))
    screen.blit(background,(0, 0))
    pygame.display.flip()

    clock=pygame.time.Clock()
    pacman_img = utils.load_image("pacman128x128.png", -1)
    #group_sprites = pygame.sprite.RenderPlain((pacman_img))

    while 1:
        clock.tick(60)

        screen.blit(background, (0, 0))
        #group_sprites.draw(screen)
        pygame.display.flip()

