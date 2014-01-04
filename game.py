#!/usr/bin/env python 

import os, sys, pygame
from pygame.locals import *

import config
import utils
import level001
import models
from menu import *

def main_menu(screen):
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('START GAME', 1, None),
                    ('EXIT', 2, None)])

    menu.set_center(True, True)
    menu.set_alignment('center', 'center')

    state = 0
    previos_state = 1

    #list for rects to update
    rect_lst = list()
    #block mouse motion for better perfomance
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    while True:
        if previos_state != state:
            background, temp = utils.load_image(os.path.join(config.img_dir,"background.jpg"))
            screen.blit(background, (0,0))
            pygame.display.flip()

            # put event to the end of the event queue
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key=0))
            previos_state = state

        #wait for new event
        ev = pygame.event.wait()

        if ev.type == pygame.KEYDOWN or ev.type == EVENT_CHANGE_STATE:
            if state == 0:
                rect_lst, state = menu.update(ev, state)
            elif state == 1:
                break
                state = 0
            else:
                pygame.quit()
                sys.exit()

        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update(rect_lst)


class Game:
    def __init__(self, width=config.screen_width, height=config.screen_height):
        # initialization all pygame modules
        pygame.init()

        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman")
        pygame.mouse.set_visible(0)
        #set repetition  (set_repeat(after first keydown, after any other))
        pygame.key.set_repeat(30,30)

        #text font
        self.font48 = pygame.font.SysFont(None, 48)
        self.font30 = pygame.font.SysFont(None, 30)

        ##sounds
        pygame.mixer.init()
        self.sounds = {'die': pygame.mixer.Sound(os.path.join(config.snd_dir, "die.ogg")),
                        'intro': pygame.mixer.Sound(os.path.join(config.snd_dir, "intro.ogg"))}

        ##intro music
        self.sounds['intro'].play()

        ##gameplay variables
        self.enemy_max_cols = 3 # equal to pacman.lives
        self.enemy_cols = 0
        self.prev_life_score = 0
        self.lives_cntr = 3
        self.max_pellets = 181
        #bool var for check enabled menu or not
        self.set_menu = False

    def __set_map(self, x_offset, y_offset, level, layout, images):
        for y in range(len(layout)):
            for x in range(len(layout[y])):
                '''Get the center point for the rects'''

                center_point = [(x*config.block_size)+x_offset, (y*config.block_size+y_offset)]
                '''
                res = {level.BLOCK:
                           self.block_sprites.add(models.BasicSprite(center_point, images[level.BLOCK])),
                       level.GWALL:
                           self.gwall_sprites.add(models.BasicSprite(center_point, images[level.GWALL])),
                       level.PACMAN:
                           self.pac.append(models.Pacman(center_point, images[level.PACMAN])),
                       level.PELLET:
                           self.pellet_sprites.add(models.BasicSprite(center_point, images[level.PELLET], colorkey=-1)),
                       level.BLINKY:
                           self.enemies.append(models.Enemy(center_point, images[level.BLINKY], colorkey=-1)),
                       level.INKY:
                           self.enemies.append(models.Enemy(center_point, images[level.INKY], colorkey=-1)),
                       level.PINKY:
                           self.enemies.append(models.Enemy(center_point, images[level.PINKY], colorkey=-1)),
                       level.CLYDE:
                           self.enemies.append(models.Enemy(center_point, images[level.CLYDE], colorkey=-1))
                }.get(layout[y][x], None)
                '''
                if layout[y][x] == level.BLOCK:
                    self.block_sprites.add(models.BasicSprite(center_point, images[level.BLOCK]))
                elif layout[y][x] == level.GWALL:
                    self.gwall_sprites.add(models.BasicSprite(center_point, images[level.GWALL]))
                elif layout[y][x] == level.PACMAN:
                    self.pacman = models.Pacman(center_point, images[level.PACMAN])
                elif layout[y][x] == level.PELLET:
                    self.pellet_sprites.add(models.BasicSprite(center_point, images[level.PELLET], colorkey=-1))
                elif layout[y][x] == level.BLINKY:
                    self.enemies.append(models.Enemy(center_point, images[level.BLINKY], colorkey=-1))
                elif layout[y][x] == level.INKY:
                    self.enemies.append(models.Enemy(center_point, images[level.INKY], colorkey=-1))
                elif layout[y][x] == level.PINKY:
                    self.enemies.append(models.Enemy(center_point, images[level.PINKY], colorkey=-1))
                elif layout[y][x] == level.CLYDE:
                    self.enemies.append(models.Enemy(center_point, images[level.CLYDE], colorkey=-1))

    def __load_sprites(self):
        x_offset = (config.block_size/2)
        y_offset = (config.block_size/2)
        ##getting layout and images for level one
        level1 = level001.level() 
        layout = level1.get_layout()
        images = level1.get_image_paths()

        self.gwall_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.pellet_sprites = pygame.sprite.Group()
        #blinky, inky, pinky, clyde
        self.enemies = list()
        self.enemies_sprites = pygame.sprite.Group()

        #self.pac = list()

        self.__set_map(x_offset, y_offset, level1, layout, images)

        #self.pacman = self.pac[0]

        self.pacman_sprite = pygame.sprite.RenderPlain((self.pacman))
        for ghost in self.enemies:
            self.enemies_sprites.add(ghost)

    def __set_backgrnd(self):
        # add background on the screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(config.BLACK)

    def __big_event_handler(self, event_text):
        self.screen.blit(self.background, (0, 0))

        utils.draw_text(event_text,
                        self.font48,
                        self.screen,
                        config.screen_width/2,
                        config.screen_height/5)

        for e in pygame.event.get():
            if e.key == ord('y'):
                #self.break_flag = True
                #we lost all lives or we won and trying to play again
                # so initialize all score variables again with zero
                self.pacman.pellets = 0
                self.pacman.score = 0
                self.prev_life_score = 0
                self.lives_cntr = 3
                self.main_loop()
            elif e.key == ord('n'):
                self.pacman.pellets = 0
                self.pacman.score = 0
                self.prev_life_score = 0
                self.lives_cntr = 3
                self.set_menu = False
                self.main_loop()

    def main_loop(self):

        self.clock = pygame.time.Clock()

        if not self.set_menu:
            self.set_menu = True
            main_menu(self.screen)

        #loading sprites
        self.__load_sprites()
        self.pacman.score = self.prev_life_score
        self.pacman.lives = self.lives_cntr
        #setting background
        self.__set_backgrnd()

        self.block_sprites.draw(self.background)
        self.gwall_sprites.draw(self.background)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type is KEYDOWN:
                    if event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                        self.pacman.move(self.block_sprites, event.key)

            # enemies random move
            for ghost in self.enemies:
                ghost.move(self.block_sprites)

            if pygame.sprite.spritecollide(self.pacman, self.enemies_sprites, False):
                #we have collision with ghost so increment ghost collision counter
                #and drop to zero number of eaten pellets
                self.enemy_cols += 1
                self.pacman.pellets = 0
                #if we lost 3 lives game over and ask for playing again
                if self.enemy_cols == self.enemy_max_cols:
                    self.enemy_cols = 0
                    while True:
                        self.__big_event_handler("You lost. Play again (y/n)?")
                        pygame.display.flip()
                #going out from loop and restart it
                break

            #check collisions True means: kill sprite from group in collision
            pacman_pellets_cols = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
            #count score 
            for dot in pacman_pellets_cols:
                self.pacman.pellets += 1
                self.pacman.score += 10
                if self.pacman.pellets == self.max_pellets:
                    while True:
                        self.__big_event_handler("You Won!!! Play again (y/n)?")
                        pygame.display.flip()

            #adding background on the screen
            self.screen.blit(self.background, (0, 0))
            
            #draw sprites
            self.pellet_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
            self.enemies_sprites.draw(self.screen)
            utils.draw_text("Score: %d "%self.pacman.score,
                            self.font30,
                            self.screen,
                            70,
                            20)
            utils.draw_text("Lives: %d "%self.lives_cntr,
                            self.font30,
                            self.screen,
                            270,
                            20)

            pygame.display.flip()
            self.clock.tick(40)

        self.sounds['die'].play()
        #we killed ,so minus one life
        #and we need to save previos score cause after start main loop below
        #self.pacman.score variable will be initialized with zero again
        self.lives_cntr -= 1
        self.prev_life_score = self.pacman.score
        self.main_loop()


