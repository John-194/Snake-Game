import pygame

from snek import Snake, Map


class App:
    def __init__(self):
        self.key = None
        self.fps = 60
        self.speedCount = 0
        self.speed = 12
        self.snake = None
        self.land = None
        self.running = True
        self.size = self.width, self.height = 500, 500
        self.scale = 1
        self.FramePerSec = pygame.time.Clock()
        try:
            pygame.init()
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        except:
            self.running = False

    # ====================================================================================================

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def loop(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # new head coords move forward
            self.key = pygame.K_w
        elif keys[pygame.K_s]:
            self.key = pygame.K_s
        elif keys[pygame.K_d]:
            self.key = pygame.K_d
        elif keys[pygame.K_a]:
            self.key = pygame.K_a

        if self.speedCount <= self.fps:
            self.speedCount += self.speed
        else:
            self.speedCount = 0
            if not self.snake.move({pygame.K_w : "w", pygame.K_s : "s", pygame.K_d : "d", pygame.K_a : "a", None :" " }[self.key]):
                self.running = False

    def render(self):
        white = pygame.Color(255, 255, 255)
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (180, 180, 0),
                         (0, 0, self.scale, self.scale))
        for r, row in enumerate(self.land.terrain):
            for c, col in enumerate(row):
                if col == " ":
                    continue
                position = [c * self.scale+self.scale//2, r * self.scale+self.scale//2]
                if col == "O":
                    if r == 0:
                        pygame.draw.rect(self.screen, (180, 180, 0),
                                         (position[0], position[1]-self.scale//2, self.scale, self.scale))
                    elif r == len(self.land.terrain)-1:
                        pygame.draw.rect(self.screen, (180, 180, 0),
                                         (position[0], position[1]-self.scale//2, self.scale, self.scale))
                    if c == 0:
                        pygame.draw.rect(self.screen, (180, 180, 0),
                                         (position[0]-self.scale//2, position[1], self.scale, self.scale))
                    elif c == len(row)-1:
                        pygame.draw.rect(self.screen, (180, 180, 0),
                                         (position[0]-self.scale//2, position[1], self.scale, self.scale))
                elif col == "S":
                    pygame.draw.circle(self.screen, (155, 155, 155), position, self.scale//2)
                elif col == "F":
                    pygame.draw.circle(self.screen, (0, 180, 180), position, self.scale//2)
                elif col == "H":
                    pygame.draw.circle(self.screen, white, position, self.scale//2)

        pygame.display.update()
        self.FramePerSec.tick(self.fps)

    # ====================================================================================================
    def execute(self):
        mapRows = 25
        print("test")
        self.scale = self.height // mapRows
        self.land = Map(mapRows, self.width//self.scale)
        self.snake = Snake(self.land)
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.loop()
            self.render()
        self.cleanup()

    @staticmethod
    def cleanup():
        pygame.quit()


app = App()
app.execute()
