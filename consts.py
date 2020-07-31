from pathlib import Path
import os
import pygame

########################################################################################################################
#                                                   PATHS                                                              #
########################################################################################################################

dirname = Path(os.path.dirname(__file__))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'bird1.png'))),
             pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'bird2.png'))),
             pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'bird3.png')))]
BG_IMG = pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'bg.png')))
FLOOR_IMG = pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'base.png')))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(str(dirname / 'imgs' / 'pipe.png')))

NEAT_CONFIG = str(dirname / 'neat_config.txt')
WINNER_FILE = str(dirname / 'winner.pkl')

########################################################################################################################
#                                                   IMG DEFAULT POSITIONS                                              #
########################################################################################################################

GAME_RES = (500, 800)
BG_POS = (0, 0)
BIRD_POS = (100, 200)

FLOOR_POS = (0, 700)
FLOOR_WIDTH = 669

PIPE_GAP = 200
PIPE_HEIGHT = 640
PIPE_TOP_MAX_Y = -550
PIPE_TOP_MIN_Y = -250
PIPE_DELETE_X_TRESHOLD = -150

########################################################################################################################
#                                                   MOVEMENT CONSTANTS                                                 #
########################################################################################################################

MAX_POSITIVE_VELOCITY = 16
GAME_SPEED = 5
