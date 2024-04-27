from pathlib import Path

import pygame
from pygame import Surface

ROOT = Path(__file__).parent.parent
RESOURCES = ROOT / 'resources'


class SPRITES:
    LEFT: Surface = None
    RIGHT: Surface = None
    TOP: Surface = None
    BOT: Surface = None
    MT: Surface = None

    MUNICH: Surface = None


def init():
    SPRITES.LEFT = pygame.image.load(RESOURCES / 'left.png').convert_alpha()
    SPRITES.RIGHT = pygame.image.load(RESOURCES / 'right.png').convert_alpha()
    SPRITES.TOP = pygame.image.load(RESOURCES / 'top.png').convert_alpha()
    SPRITES.BOT = pygame.image.load(RESOURCES / 'bot.png').convert_alpha()
    SPRITES.MT = pygame.image.load(RESOURCES / 'mt.png').convert_alpha()

    SPRITES.MUNICH = pygame.image.load(RESOURCES / 'munich1.png').convert_alpha()
