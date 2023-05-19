import pygame

pygame.init()

screen = pygame.display.set_mode((900, 700))
Clock = pygame.time.Clock()

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.Surface((300, 10))
        pygame.draw.rect(self.img, (0, 255, 0), (0, 0, 100, 20))
        self.in_move = 0
        self.vy = 0
        self.a = 0.1

    def draw(self):
        rect = self.img.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(self.img, rect)

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def gravity(self, floor):
        if self.y < floor:
              self.move(0, self.vy)
              self.vy += self.a
        else:
              self.y = floor
              self.vy = 0

box = Box(150, 800)
keys = set()
while True:
    Clock.tick(400)
    screen.fill((0, 0, 0))
    box.gravity(500)
    box.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
             if event.key == 97:
                     box.in_move = -1
                     keys.add(97)
             if event.key == 100:
                     box.in_move = 1
                     keys.add(100)
             if event.key == 32:
                     box.move(0, -1)
                     box.vy = -10


        if event.type == pygame.KEYUP:
                  keys.discard(event.key)
                  if not keys:
                         box.in_move = 0
    if box.in_move == 1:
       box.move(1, 0)
    if box.in_move == -1:
       box.move(-1, 0)
    if box.x > 1050:
       box.x = 150
       box.y = 500

    pygame.display.update()