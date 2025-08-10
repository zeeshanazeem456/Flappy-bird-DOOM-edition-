from collections import deque
import pygame as pg
from settings import Settings

class BackGround:
    def __init__(self, game):
        self.game = game
        self.settings = Settings()
        self.speed = self.settings.Scrolling_Speed - 2

        # Setup all images in a deque (to rotate easily)
        self.images = deque([
            self.game.background_1,
            self.game.background_2,
            self.game.background_3
        ])

        self.bg_width = self.settings.WIDTH  # assuming all images are the same width
        self.x = 0  # Scroll position

        # Background image A and B
        self.bg1 = self.images[0]
        self.bg2 = self.images[1]

    def update(self):
        self.x -= self.speed

        # Once the first image fully goes off-screen, rotate to the next pair
        if self.x <= -self.bg_width:
            self.x = 0
            self.images.rotate(-1)
            self.bg1 = self.images[0]
            self.bg2 = self.images[1]

    def draw(self):
        self.game.SCREEN.blit(self.bg1, (self.x, 0))
        self.game.SCREEN.blit(self.bg2, (self.x + self.bg_width, 0))

class Ground(BackGround):
    def __init__(self, game):
        super().__init__(game)
        self.y = self.settings.GROUND_Y
        self.speed = self.settings.Scrolling_Speed
        self.image = self.game.ground_image


    def update(self):
        self.x = (self.x - self.speed) % -self.settings.WIDTH

    def draw(self):
        self.game.SCREEN.blit(self.image,(self.x,self.y))
        self.game.SCREEN.blit(self.image,(self.settings.WIDTH + self.x,self.y))

class Sound:
    def __init__(self):
        self.hit_sound = pg.mixer.Sound('assets/sound/hit.wav')
        self.point_sound = pg.mixer.Sound('assets/sound/point.wav')
        self.wing_sound = pg.mixer.Sound('assets/sound/wing.wav')
        self.Theme_song = pg.mixer.Sound('assets/Theme_song.mp3')

class Score:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.font = pg.font.Font('assets/font/doom.ttf', 150)
        self.font_pos = (self.settings.WIDTH // 2, self.settings.HEIGHT // 8)

    def draw(self):
        score = self.game.pipe_handler.passed_pipes
        self.text = self.font.render(f'{score}', True, 'white')
        self.game.SCREEN.blit(self.text, self.font_pos)


