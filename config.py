
# configuration file

import os

base_dir = os.path.normpath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, "data")
img_dir = os.path.join(data_dir, "img")
snd_dir = os.path.join(data_dir, "snd")
pacman_dir = os.path.join(img_dir,"pacman")
enemy_dir = os.path.join(img_dir,"enemy")

BLACK = (0, 0, 0)
WHITE = (255,255,255)

screen_width = 500
screen_height = 575
block_size = 24
