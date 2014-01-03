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
                 [('start game', 1, None),
                    ('exit', 2, None)])

class Game:
    def __init__(self, width = config.screen_width, height = config.screen_height):
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
        self.enemy_max_cols = 3
        self.enemy_cols = 0
        self.prev_life_score = 0
        #magic break const for manipulation with user actions
        self.break_flag = False

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

        for y in range(len(layout)):
            for x in range(len(layout[y])):

                """Get the center point for the rects"""

                center_point = [(x*config.block_size)+x_offset, (y*config.block_size+y_offset)]
                if layout[y][x] == level1.BLOCK:
                    self.block_sprites.add(models.BasicSprite(center_point, images[level1.BLOCK]))
                elif layout[y][x] == level1.GWALL:
                    self.gwall_sprites.add(models.BasicSprite(center_point, images[level1.GWALL]))
                elif layout[y][x] == level1.PACMAN   :
                    self.pacman = models.Pacman(center_point, images[level1.PACMAN])
                elif layout[y][x] == level1.PELLET:
                    self.pellet_sprites.add(models.BasicSprite(center_point, images[level1.PELLET], colorkey=-1))
                elif layout[y][x]==level1.BLINKY:
                    self.blinky = models.Enemy(center_point, images[level1.BLINKY], colorkey=-1)
                elif layout[y][x]==level1.INKY:
                    self.inky = models.Enemy(center_point, images[level1.INKY], colorkey=-1)
                elif layout[y][x]==level1.PINKY:
                    self.pinky = models.Enemy(center_point, images[level1.PINKY], colorkey=-1)
                elif layout[y][x]==level1.CLYDE:
                    self.clyde = models.Enemy(center_point, images[level1.CLYDE], colorkey=-1)

        self.pacman_sprite = pygame.sprite.RenderPlain((self.pacman))
        self.blinky_sprite = pygame.sprite.RenderPlain((self.blinky))
        self.inky_sprite = pygame.sprite.RenderPlain((self.inky))
        self.pinky_sprite = pygame.sprite.RenderPlain((self.pinky))
        self.clyde_sprite = pygame.sprite.RenderPlain((self.clyde))

    def __set_backgrnd(self):
        # add background on the screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(config.BLACK)

    def main_loop(self):
        #getting clock to control frame rate
        self.clock = pygame.time.Clock()
        
        #loading sprites
        self.__load_sprites()
        self.pacman.score = self.prev_life_score
        #setting background
        self.__set_backgrnd()

        self.block_sprites.draw(self.background)
        self.gwall_sprites.draw(self.background)

        while True:
            self.break_flag = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type is KEYDOWN:
                    if event.key == K_RIGHT \
                            or event.key == K_LEFT \
                            or event.key == K_UP \
                            or event.key == K_DOWN:
                                self.pacman.move(self.block_sprites, event.key)

            # enemies random move
            self.blinky.move(self.block_sprites)
            self.inky.move(self.block_sprites)
            self.clyde.move(self.block_sprites)
            self.pinky.move(self.block_sprites)

            if pygame.sprite.collide_rect(self.blinky, self.pacman) or\
                pygame.sprite.collide_rect(self.inky, self.pacman) or\
                pygame.sprite.collide_rect(self.clyde, self.pacman) or\
                pygame.sprite.collide_rect(self.pinky, self.pacman):
                self.enemy_cols += 1
                #if we lost 3 lives game over and ask for playing again
                if self.enemy_cols == self.enemy_max_cols:
                    self.enemy_cols = 0
                    while True:
                        self.screen.blit(self.background, (0, 0))

                        utils.draw_text("Play again?",
                                        self.font48,
                                        self.screen,
                                        config.screen_width/2,
                                        config.screen_height/5)
                        for e in pygame.event.get():
                            if e.key == ord('y'):
                                self.break_flag = True
                                self.pacman.pellets = 0
                                self.pacman.score = 0
                                self.prev_life_score = 0
                            elif e.key == ord('n'):
                                pygame.quit()
                                sys.exit()
                        if self.break_flag:
                            break
                        pygame.display.flip()

                    #sys.exit()
                #going out from loop and restart it
                break

            #check collisions True means: kill sprite from group in collision
            pacman_pellets_cols = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
            #count score 
            for dot in pacman_pellets_cols:
                self.pacman.pellets += 1
                self.pacman.score += 10

            #adding background on the screen
            self.screen.blit(self.background, (0, 0))
            
            #draw sprites
            self.pellet_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
            self.blinky_sprite.draw(self.screen)
            self.pinky_sprite.draw(self.screen)
            self.inky_sprite.draw(self.screen)
            self.clyde_sprite.draw(self.screen)

            utils.draw_text("Score: %d "%self.pacman.score,
                            self.font30,
                            self.screen,
                            70,
                            20)

            pygame.display.flip()
            self.clock.tick(40)
        if  not self.break_flag:
            self.sounds['die'].play()
            self.prev_life_score = self.pacman.score
        self.main_loop()



