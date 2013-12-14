#/usr/bin/env python

import os, pygame
from pygame.locals import *

#functions to create our resources
def load_image(fullname, colorkey=None):
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print ("Cannot load image:%s"% fullname)
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


