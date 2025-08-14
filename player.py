import pygame as pg
from settings import Settings
from collections import deque

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.sprites_group)
        self.Music_Flag = True
        self.game = game
        self.settings = Settings()
        self.image = game.bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.settings.BIRD_POSITION
        self.images = deque(game.bird_images)
        #Initializing a custom event (This event will let us know when it is time for it to trigger)
        self.animation_event = pg.USEREVENT + 0
        self.mask = pg.mask.from_surface(game.mask_image)
        #Here we get a timer for our event(to let us know when to change frames)
        pg.time.set_timer(self.animation_event,self.settings.animation_time)
        self.falling_velocity = 0
        self.first_jump = False
        self.angle = 0

    def check_collision(self):
        hit = pg.sprite.spritecollide(self,self.game.pipes,dokill = False,collided = pg.sprite.collide_mask)
        if hit or self.rect.bottom > self.settings.GROUND_Y + 10 or self.rect.top < -self.image.get_height():
            self.game.sound.Theme_song.stop()
            self.game.sound.hit_sound.play()
            self.first_jump = False
            pg.time.wait(1000)
            self.game.first_dead = not self.game.first_dead
            self.game.new_game()

    def rotate(self):
        if self.first_jump:
            # Tilt up on jump, tilt down as falling increases
            if self.falling_velocity < -self.settings.jump_height:
                self.angle = self.settings.BIRD_ANGLE  # e.g. 25
            else:
                self.angle = max(-2.5 * self.falling_velocity, -90)  # cap at -90 degrees

            # Rotate the original (current animation frame), not the already rotated image
            rotated_image = pg.transform.rotate(self.images[0], self.angle)
            self.image = rotated_image

            # Optional: Adjust position so rotation doesn't offset bird too far
            self.rect = self.image.get_rect(center=self.rect.center)
            mask_image = pg.transform.rotate(self.game.mask_image, self.angle)
            self.mask = pg.mask.from_surface(mask_image)


    def jump(self):
        self.game.sound.wing_sound.play()
        self.falling_velocity = self.settings.jump_height

    def impliment_gravity(self):
        if self.first_jump:
            self.falling_velocity += self.settings.gravity
            self.rect.y += self.falling_velocity #* 0.5 * self.settings.gravity

    def update(self):
        self.check_collision()
        self.impliment_gravity()
        self.rotate()

    def animate(self):
        self.images.rotate(-1)
        self.image = self.images[0]

    def check_event(self,event):
        #Here we check if our event is triggered
        if event.type == self.animation_event:
            self.animate()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if self.Music_Flag:
                self.game.sound.Theme_song.play()
                self.Music_Flag = False
            self.first_jump = True
            self.jump()

    def update_images(self, new_images):
        self.images = new_images
        self.image = self.images[0]

