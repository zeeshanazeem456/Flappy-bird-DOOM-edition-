class Settings:
    def __init__(self):
        self.HEIGHT = 600
        self.WIDTH = 1000
        self.FPS = 60
        self.Scrolling_Speed = 5

        #bird settings
        self.BIRD_POSITION = self.WIDTH // 4, self.HEIGHT//3
        self.IMAGE_SCALE = 1
        self.animation_time = 150
        self.SCALE = 1
        self.jump_height = -13
        self.BIRD_ANGLE = 25
        #ground
        self.GROUND_HEIGHT = self.HEIGHT //12
        self.GROUND_Y = self.HEIGHT - self.GROUND_HEIGHT
        self.gravity = 1
        #Pipe
        self.PIPE_WIDTH = 200 
        self.PIPE_HEIGHT = self.HEIGHT
        self.Distance_between_pipes = 650
        self.GAP_HEIGHT = 300
        self.HALF_GAP_HEIGHT = self.GAP_HEIGHT // 2