import sys
import pygame as pg
from player import Player
from pipes import *
from game_objects import *
from settings import Settings
from pipes import *
from fire import *

class FlappyBird:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.SCREEN = pg.display.set_mode((self.settings.WIDTH,self.settings.HEIGHT))
        self.clock = pg.time.Clock()
        self.sound = Sound()
        self.fire = DoomFire(self)
        self.score = Score(self)
        self.first_dead = False
        self.mask_flag = False
        self.player_flag = False
        self.load_assets()
        self.new_game()

    def load_assets(self):
        #Loading player
        self.bird_images = [pg.image.load(f'assets/bird/{index}.png').convert_alpha() for index in range(5)]
        #Scaling our player
        bird_image = self.bird_images[0]
        bird_size = bird_image.get_width() * self.settings.IMAGE_SCALE,bird_image.get_height() * self.settings.IMAGE_SCALE
        self.bird_images = [pg.transform.scale(sprite,bird_size) for sprite in self.bird_images]
        #Loading bg
        self.background_1 = pg.image.load('assets/images/walls/0.jpg').convert()
        self.background_2 = pg.image.load('assets/images/walls/1.jpg').convert()
        self.background_3 = pg.image.load('assets/images/walls/2.jpg').convert()
        #scaling our background
        self.background_1 = pg.transform.scale(self.background_1,(self.settings.WIDTH,self.settings.HEIGHT))
        self.background_2 = pg.transform.scale(self.background_2,(self.settings.WIDTH,self.settings.HEIGHT))
        self.background_3 = pg.transform.scale(self.background_3,(self.settings.WIDTH,self.settings.HEIGHT))
        #Ground
        self.ground_image = pg.image.load('assets/images/ground.png')
        self.ground_image = pg.transform.scale(self.ground_image,(self.settings.WIDTH,self.settings.GROUND_HEIGHT))
        #pipes
        # pipes
        self.top_pipe_image = pg.image.load('assets/images/top_pipe.png').convert_alpha()
        self.top_pipe_image = pg.transform.scale(self.top_pipe_image, (self.settings.PIPE_WIDTH, self.settings.PIPE_HEIGHT))
        self.bottom_pipe_image = pg.transform.flip(self.top_pipe_image, False, True)
        #player mask
        mask_image = pg.image.load('assets/bird/mask.png').convert_alpha()
        mask_size = mask_image.get_width() * self.settings.SCALE, mask_image.get_height() * self.settings.SCALE
        self.mask_image = pg.transform.scale(mask_image, mask_size)


    def change_player(self):
        self.settings.IMAGE_SCALE = 2
        self.bird_images = [pg.image.load(f'assets/bird_1/{index}.png').convert_alpha() for index in range(5)]
        bird_image = self.bird_images[0]
        bird_size = bird_image.get_width() * self.settings.IMAGE_SCALE,bird_image.get_height() * self.settings.IMAGE_SCALE
        self.bird_images = [pg.transform.scale(sprite,bird_size) for sprite in self.bird_images]
        self.player.update_images(deque(self.bird_images))

    def change_player_1(self):
        self.settings.IMAGE_SCALE = 1
        self.bird_images = [pg.image.load(f'assets/bird/{index}.png').convert_alpha() for index in range(5)]
        #Scaling our player
        bird_image = self.bird_images[0]
        bird_size = bird_image.get_width() * self.settings.IMAGE_SCALE,bird_image.get_height() * self.settings.IMAGE_SCALE
        self.bird_images = [pg.transform.scale(sprite,bird_size) for sprite in self.bird_images]
        self.player.update_images(deque(self.bird_images))

    def new_game(self):
        if self.first_dead:
            self.change_player()
        if not self.first_dead:
            self.settings.IMAGE_SCALE = 1
            self.bird_images = [pg.image.load(f'assets/bird/{index}.png').convert_alpha() for index in range(5)]
            bird_image = self.bird_images[0]
            bird_size = bird_image.get_width() * self.settings.IMAGE_SCALE,bird_image.get_height() * self.settings.IMAGE_SCALE
            self.bird_images = [pg.transform.scale(sprite,bird_size) for sprite in self.bird_images]
        self.sprites_group = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.player = Player(self)
        self.bg = BackGround(self)
        self.ground = Ground(self)
        self.pipe_handler = PipeHandler(self)

    def draw(self):
        self.bg.draw()
        self.fire.draw()
        self.sprites_group.draw(self.SCREEN)
        self.ground.draw()  
        self.score.draw()
        #pg.draw.rect(self.SCREEN,'yellow',self.player.rect, 4) 
        if self.mask_flag: 
            self.player.mask.to_surface(self.SCREEN,unsetcolor = None,dest = self.player.rect,setcolor = 'green')
        pg.display.flip()

    def update(self):
        self.sprites_group.update()
        self.bg.update()
        self.fire.update()
        self.ground.update()
        self.pipe_handler.update()
        self.clock.tick(self.settings.FPS)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.mask_flag = not self.mask_flag
                if event.key == pg.K_z:
                    self.player_flag = not self.player_flag
                    if self.player_flag:
                        self.change_player()
                    else:
                        self.change_player_1()
            self.player.check_event(event)

    def run(self):
        while(True):
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = FlappyBird()
    game.run()
