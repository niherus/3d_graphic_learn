import pygame
import math
from random import randint as rnd

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()

class Camera:
    def __init__(self, x, y, z, dr):
        self.pos = (x, y, z)
        self.dr = dr
        self.wall = 800
        self.dist = 400
    
    def move(self, dx, dz):
        x, y, z = self.pos
        self.pos = (x + dx, y, z + dz)
    
    def rotate(self, da):
        x, y = self.dr
        self.dr = (x * math.cos(da) - y * math.sin(da), x * math.sin(da) + y * math.cos(da))
        
    def render(self):
        k = self.pos[2] / self.dist
        if k > 1:
            k = 1
        pygame.draw.rect(screen, (200, 200, 200), ((400, (HEIGHT - self.wall * k) // 2 ), (200, self.wall * k )))
        
player = Camera(0, 0, 0, (0, 1))

render = True
mz = 0
keys = set()
while render:
    clock.tick(60)
    pygame.display.set_caption(f"FPS: {clock.get_fps()}")
    screen.fill((0, 0, 0))
    player.render()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False
            break
        if ev.type == pygame.KEYDOWN:
            if ev.key == 119:
                mz = 5
                keys.add(119)
            if ev.key == 115:
                mz = -5
                keys.add(115)

        if ev.type == pygame.KEYUP:
            keys.discard(ev.key)

            if not keys:
                mz = 0
        
        if ev.type == pygame.MOUSEMOTION:
            player.rotate(ev.rel[0])
            print(player.dr)

    player.move(0, mz)   
 
    pygame.display.update()
exit()
