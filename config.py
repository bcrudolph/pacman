
# configuration file

import os

base_dir = os.path.normpath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, "data")
img_dir = os.path.join(data_dir, "img")
pacman_dir = os.path.join(img_dir,"pacman")
enemy_dir = os.path.join(img_dir,"enemy")

screen_width = 640
screen_height = 480

portal_width = 20
aisle_width = 25
aisle_height = 25
