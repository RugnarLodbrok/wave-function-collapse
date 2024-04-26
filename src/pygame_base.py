from functools import reduce
from operator import add
from typing import Callable, Self

import pygame
from pygame import Surface, Vector2
from py_tools.time_utils import swatch
from time import time

from pygame.event import Event
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from src.resources import init as load_resources


class GameObject:
    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: Surface):
        pass


class Game:
    def __init__(self):
        self.objects: list[GameObject] = []
        self._running = False
        self._initialized = False
        self.screen: Surface | None = None
        self.fill = (255, 255, 255)
        self.key_map: dict[int: Callable[[Self], None]] = {}

    def _update(self, dt: float):
        for obj in self.objects:
            obj.update(dt)

    def _info(self):
        pass

    def _draw(self):
        screen = self.screen
        if fill := self.fill:
            screen.fill(fill)
        for obj in self.objects:
            obj.draw(screen)
        pygame.display.flip()

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1280, 1280])
        load_resources()
        self._initialized = True

    def run(self, fps: float = 60):
        if not self._initialized:
            self.initialize()
        self._running = True
        draw_dt = 1 / fps
        info_dt = 1
        swatch()
        last_draw_t = 0
        last_info_t = 0
        while self._running:
            # swatch.wait(target_dt)
            dt = swatch()
            self._update(dt)

            if swatch.t - last_draw_t > draw_dt:
                last_draw_t = swatch.t
                self.process_events()
                self._draw()
            if swatch.t - last_info_t > info_dt:
                last_info_t = swatch.t
                self._info()
        pygame.quit()

    def process_events(self):
        event: Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self._running = False
                elif key in self.key_map:
                    self.key_map[key](self)
