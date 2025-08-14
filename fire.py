import pygame as pg
from pygame import gfxdraw
from random import randint
from settings import *

STEPS_BETWEEN_COLORS = 4
COLORS = ['black', 'green', 'orange', 'yellow', 'white']
PIXEL_SIZE = 4

FIRE_REPS = 4

class DoomFire:
    def __init__(self, app):
        self.app = app
        self.settings = Settings()
        self.FIRE_WIDTH = self.settings.WIDTH // (PIXEL_SIZE * FIRE_REPS)
        self.FIRE_HEIGHT = self.settings.HEIGHT // PIXEL_SIZE + 20
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pg.Surface([PIXEL_SIZE * self.FIRE_WIDTH, self.settings.HEIGHT])

        self.fire_screen_surf = pg.Surface((self.settings.WIDTH,self.settings.HEIGHT))
        self.fire_screen_surf.set_colorkey('black')
        self.speed = self.settings.Scrolling_Speed
        self.x = 0

    def do_fire(self):
        for x in range(self.FIRE_WIDTH):
            for y in range(1, self.FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % self.FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        self.fire_surf.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                  PIXEL_SIZE, PIXEL_SIZE), color)

        for i in range(FIRE_REPS):
            self.fire_screen_surf.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))
        # draw final fire
        self.app.SCREEN.blit(self.fire_screen_surf, (self.x, -self.settings.GROUND_HEIGHT))
        self.app.SCREEN.blit(self.fire_screen_surf, (self.settings.WIDTH + self.x, -self.settings.GROUND_HEIGHT))

    def get_fire_array(self):
        fire_array = [[0 for i in range(self.FIRE_WIDTH)] for j in range(self.FIRE_HEIGHT)]
        for i in range(self.FIRE_WIDTH):
            fire_array[self.FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def move_fire(self):
        self.x = (self.x - self.speed) % -self.settings.WIDTH

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pg.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def update(self):
        self.do_fire()
        self.move_fire()

    def draw(self):
        self.draw_fire()