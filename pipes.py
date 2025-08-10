import pygame as pg
from random import randint
from settings import Settings

class TopPipe(pg.sprite.Sprite):
    def __init__(self,app,gap_y):
        super().__init__(app.pipes,app.sprites_group)
        self.settings = Settings()
        self.image = app.top_pipe_image
        self.rect = app.top_pipe_image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.bottomleft = self.settings.WIDTH,gap_y - self.settings.HALF_GAP_HEIGHT - self.settings.GROUND_HEIGHT

    def update(self):
        self.rect.left -= self.settings.Scrolling_Speed
        if self.rect.right < 0:
            self.kill()

class BottomPipe(TopPipe):
    def __init__(self, app, gap_y_pos):
        super().__init__(app, gap_y_pos)
        self.settings = Settings()
        self.image = app.bottom_pipe_image
        self.rect.topleft = self.settings.WIDTH, gap_y_pos + self.settings.HALF_GAP_HEIGHT - self.settings.GROUND_HEIGHT


class PipeHandler:
    def __init__(self,game):
        self.game = game
        self.settings = Settings()
        self.pipe_dist = self.settings.Distance_between_pipes
        self.pipes = []
        self.passed_pipes = 0

    def count_passed_pipes(self):
        for pipe in self.pipes:
            if self.game.settings.BIRD_POSITION[0] >pipe.rect.right:
                self.game.sound.point_sound.play()
                self.passed_pipes += 1
                self.pipes.remove(pipe)

    def update(self):
        self.generate_pipes()
        self.count_passed_pipes()

    def generate_pipes(self):
        if self.game.player.first_jump:
            self.pipe_dist += self.settings.Scrolling_Speed
            if self.pipe_dist > self.settings.Distance_between_pipes:
                self.pipe_dist = 0
                gap_y = self.get_gap()
                TopPipe(self.game,gap_y)
                pipe = BottomPipe(self.game,gap_y)
                self.pipes.append(pipe)

    def get_gap(self):
        return randint(
            self.settings.GAP_HEIGHT,
            self.settings.HEIGHT - self.settings.GAP_HEIGHT
        )

