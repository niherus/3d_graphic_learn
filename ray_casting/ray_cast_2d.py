import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()

class Rays:
    
    def __init__(self, x, y, dr):
        self.pos = x, y

        self.dr = self.norm(dr)
        self.range = 1000
        self.fov = 120
        self.res = 10
    
    def cast(self, objects):
        x, y = self.pos
        dx, dy = self.norm(self.dr)
        
        for i in range(-self.fov // 2 * self.res, self.fov // 2 * self.res):
            theta = math.pi * i / (180 * self.res) 
            dist = self.range ** 2
            ddx, ddy = dx * math.cos(theta) - dy * math.sin(theta), dx * math.sin(theta) + dy * math.cos(theta)
            end = x + ddx * self.range, y + ddy * self.range
            for obj in objects:
                new_end = obj.cut_vector((self.pos, end))
                if dist > (new_end[0] - x) ** 2 + (new_end[1] - y) ** 2:
                    end = new_end
                    dist = (new_end[0] - x) ** 2 + (new_end[1] - y) ** 2
            pygame.draw.line(screen, (255, 0, 0), self.pos, end)
        
    def move(self, dx, dy):
        x, y = self.pos
        self.pos = x + dx, y + dy
        
    def norm(self, vec):
        dx, dy = vec
        d = math.hypot(dx, dy)
        return dx / d, dy / d
    
class RectObj:
    def __init__(self, x, y, w=200, h=100):

        self.size = w, h
        self.pos = x - w // 2, y + h // 2
    
    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.pos, self.size))
    
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

               end = d1 / d, d2 / d
               if dist > (st1[0] - end[0]) ** 2 + (st1[1] - end[1]) ** 2:
                   final_end = end
                   dist = (st1[0] - end[0]) ** 2 + (st1[1] - end[1]) ** 2

        return final_end

    
rays = Rays(300, 900, (0, 1))   
box = RectObj(500, 800)
render = True
press = False
mx = 0
my = 0
keys = set()

while render:
    clock.tick(60)
    pygame.display.set_caption(f"FPS: {clock.get_fps()}")
    screen.fill((0, 0, 0))
    rays.cast([box])
    box.draw()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False
            break
        
        if ev.type == pygame.MOUSEMOTION:
            x1, y1 = rays.pos
            x2, y2 = ev.pos
            rays.dr = (x2 - x1, y2 - y1)
            
            
        if ev.type == pygame.KEYDOWN:
            if ev.key == 100:
                mx = 2
                keys.add(100)
                
            if ev.key == 97:
                mx = -2
                keys.add(97)
                
            if ev.key == 115:
                my = 2
                keys.add(115)
                
            if ev.key == 119:
                my = -2
                keys.add(119)
                
        if ev.type == pygame.KEYUP:
            keys.discard(ev.key)
            if 100 not in keys and 97 not in keys:
                mx = 0
            if 115 not in keys and 119 not in keys:
                my = 0
                

    rays.move(mx, my)
    pygame.display.update()
exit()