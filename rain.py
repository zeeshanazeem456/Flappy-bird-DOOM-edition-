import pygame as pg
import random

class Raindrop:
    def __init__(self, window, screen_height):
        self.x = random.randint(5, 1000)
        self.y = random.randint(-1500, 0)
        self.zaxis = random.randint(0, 20)
        self.width = random.randint(1, 3)
        self.length = self.map_value(self.zaxis, 0, 20, 10, 30)
        self.yspeed = self.map_value(self.zaxis, 0, 20, 0.5, 2)
        self.color = (139, 0, 0)
        self.window = window
        self.screen_height = screen_height

    def fall(self):
        self.y += self.yspeed
        self.yspeed += (0.005 * self.zaxis) / 30
        if self.y >= self.screen_height:
            self.y = random.randint(-200, -100)
            self.yspeed = self.map_value(self.zaxis, 0, 20, 0.5, 2)

    def display(self):
        pg.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.length))

    def map_value(self, x, x1, x2, y1, y2):
        return y1 + x * (y2 - y1) / (x2 - x1)


class RainEffect:
    def __init__(self, window, screen_size, num_drops=300):
        self.window = window
        self.screen_width, self.screen_height = screen_size
        self.drops = [Raindrop(window, self.screen_height) for _ in range(num_drops)]

    def update(self):
        for drop in self.drops:
            drop.fall()

    def draw(self):
        for drop in self.drops:
            drop.display()
