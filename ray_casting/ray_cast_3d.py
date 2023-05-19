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
        self.range = 400
        self.fov = 120
        self.res = 1
    
    def move(self, dx, dz):
        x, y, z = self.pos
        self.pos = (x + dx, y, z + dz)
    
    def rotate(self, da):
        x, y = self.dr
        self.dr = (x * math.cos(da) - y * math.sin(da), x * math.sin(da) + y * math.cos(da))
        
    def render(self, objects):
        for i in range(-self.fov // 2 * self.res, self.fov // 2 * self.res):
            theta = math.pi * i / (180 * self.res) 
            dist = self.range ** 2
            dx, dy = self.dr
            ddx, ddy = dx * math.cos(theta) - dy * math.sin(theta), dx * math.sin(theta) + dy * math.cos(theta)
            end = x + ddx * self.range, y + ddy * self.range
            flag = False
            for obj in objects:
                new_end = obj.cut_vector((self.pos, end))
                if dist > (new_end[0] - x) ** 2 + (new_end[2] - y) ** 2:
                    end = new_end
                    dist = (new_end[0] - x) ** 2 + (new_end[2] - y) ** 2
                    flag = True
            if flag:
                k = math.sqrt((self.pos[0] - end[0]) ** 2 + ( self.pos[2] - end[0]) ** 2) 
            #if k > 1:
            #    k = 1
            #pygame.draw.rect(screen, (200, 200, 200), ((400, (HEIGHT - self.wall * k) // 2 ), (200, self.wall * k )))
 
 
class Wall:
    
    def __init__(self, x, z, w, d):
        self.pos = (x, z)
        self.size = (w, d)
    
    def cut_vector(self, cvec):
        st1, end1 = cvec
        x11, y11, x12, y12 = *st1, *end1

        a1 = - (y11 - y12)
        b1 = (x11 - x12)
        c1 =  - y11 * (x11 - x12) + x11 *  (y11 - y12)
        final_end = end1
        dist = (st1[0] - final_end[0]) ** 2 + (st1[1] - final_end[1]) ** 2
        
        for bvec in [((self.pos[0],  self.pos[1]), (self.pos[0] + self.size[0],  self.pos[1])),
                     ((self.pos[0],  self.pos[1]), (self.pos[0],  self.pos[1] + self.size[1])),
                     ((self.pos[0] + self.size[0],  self.pos[1] + self.size[1]), (self.pos[0],  self.pos[1] + self.size[1])),
                     ((self.pos[0] + self.size[0],  self.pos[1] + self.size[1]), (self.pos[0] + self.size[0],  self.pos[1])),
                     ]:
   
            st2, end2 = bvec
            x21, y21, x22, y22 = *st2, *end2

            a2 = - (y21 - y22)
            b2 = (x21 - x22)
            c2 =  - y21 * (x21 - x22) + x21 *  (y21 - y22)

            if (a1 * x21 + b1 * y21 + c1 ) * (a1 * x22 + b1 * y22 + c1) <= 0 and (a2 * x11 + b2 * y11 + c2 ) * (a2 * x12 + b2 * y12 + c2) <= 0:
               d = a1 * b2 - a2 * b1
               d1 = -c1 * b2 - -c2 * b1
               d2 = a1 * -c2 - a2 * -c1
               if d:
                   end = d1 / d, d2 / d
                   if dist > (st1[0] - end[0]) ** 2 + (st1[1] - end[1]) ** 2:
                       final_end = end
                       dist = (st1[0] - end[0]) ** 2 + (st1[1] - end[1]) ** 2

        return final_end
        

player = Camera(0, 0, 0, (0, 1))
walls = [Wall(100, 100, 500, 10)]

render = True
mz = 0
keys = set()
while render:
    clock.tick(60)
    pygame.display.set_caption(f"FPS: {clock.get_fps()}")
    screen.fill((0, 0, 0))
    player.render(walls)
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
