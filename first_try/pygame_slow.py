import pygame
import numpy as np
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

class Cube:
    def __init__(self, x, y, z, w=100, h=100, d=100):
        self.center = (x, y, z)
        
        self.size = (w, h, d)
        self.vertexes = [
            (-w // 4, -h // 2, -d // 2), 
            (-w // 4, -h // 2, d // 2), 
            (-w // 4, h // 2, -d // 2), 
            (-w // 4, h // 2, d // 2), 
            (w // 4, -h // 2, -d // 2), 
            (w // 4, -h // 2,  d // 2), 
            (w // 4, h // 2, -d // 2), 
            (w // 4, h // 2, d // 2), 
            
        ]
        self.alpha = 0
        self.vert_to_draw = self.place(self.vertexes)
        self.edges  = [
            (0, 1), 
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]
    def place(self, vertexes):
        return [(self.center[0] + x, self.center[1] + y, self.center[2] + z) for x, y, z in vertexes]
    def move(self, dx, dy, dz):
         self.center = (self.center[0] + dx, self.center[1] + dy, self.center[2] + dz)
         
         
    
    def rotate(self, alpha):
        '''
        return [(
            x * np.cos(alpha) - y * np.sin(alpha),
            x * np.sin(alpha) + y * np.cos(alpha),
            z ) for x, y, z in self.vertexes]
        return [(
            x * np.cos(alpha) + z * np.sin(alpha),
            y,
            -x * np.sin(alpha) + z * np.cos(alpha)
            ) for x, y, z in self.vertexes]
        '''
        return [(
            x,
            y * np.cos(alpha) - z * np.sin(alpha),
            y * np.sin(alpha) + z * np.cos(alpha),
            ) for x, y, z in self.vertexes]

    def update(self):
        self.vert_to_draw = self.place(self.rotate(self.alpha))
        
class Camera:
    def __init__(self, x=0, y=0, z=0, dist=50):
        self.center = (x, y, z)
        self.view = (1, 0, 0)
        self.dist = dist
    
    def get_linefunc(self, point):
        func = []
        for i in range(3):
            func.append((self.center[i] - point[i], point[i]))           
        return func
    
    def get_projection(self, point):
        line = self.get_linefunc(point)
        if point[1] and point[2]:
            dmat = np.array([
                self.view,
                (line[1][0], -line[0][0], 0),
                (0, line[2][0], -line[1][0]),
            ])
            shift = np.array([
                self.dist,
                line[1][0] * line[0][1] - line[0][0] * line[1][1],
                line[2][0] * line[1][1] - line[1][0] * line[2][1]
            ])
        elif point[1]:
            dmat = np.array([
                self.view,
                (line[1][0], -line[0][0], 0),
                (line[2][0], 0, -line[0][0]),
            ])
            shift = np.array([
                self.dist,
                line[1][0] * line[0][1] - line[0][0] * line[1][1],
                line[2][0] * line[0][1] - line[0][0] * line[2][1]
            ])
        elif point[2]:
            dmat = np.array([
                self.view,
                (line[1][0], -line[0][0], 0),
                (line[2][0], 0, -line[0][0]),
            ])
            shift = np.array([
                self.dist,
                line[1][0] * line[0][1] - line[0][0] * line[1][1],
                line[2][0] * line[0][1] - line[0][0] * line[2][1]
            ])
        else:
            dmat = np.array([
                
                self.view,
                (line[1][0], -line[0][0], 0),
                (line[2][0], 0, -line[0][0]),
            ])
            shift = np.array([
                self.dist,
                line[1][0] * line[0][1] - line[0][0] * line[1][1],
                line[2][0] * line[0][1] - line[0][0] * line[2][1]
            ])
        try:
            return np.linalg.solve(dmat, shift)
        except:
            return (0, 0, 0)
    def look_at(self, obj):
        vertexes = [self.get_projection(vertex) for vertex in obj.vert_to_draw]


        for edge in obj.edges:
            v1, v2 = edge
            _, x1, y1 = vertexes[v1]
            _, x2, y2 = vertexes[v2]
            pygame.draw.line(screen, (0, 255, 0), (500 + x1, 500 + y1), (500 + x2, 500 + y2 ))
        for vertex in vertexes:
            _, x, y = vertex
            pygame.draw.circle(screen, (255, 0, 0), (500 + x, 500 + y), 5)
    

                  
b = Cube(150, 0, 0)
camera = Camera()
b.alpha = 0

render = True
while render:
    clock.tick(60)
    screen.fill((0, 0, 0))
    b.update()
    camera.look_at(b)
    b.alpha += 0.1
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False
            exit()
        if ev.type == pygame.MOUSEMOTION:
            if ev.rel[0] > 0 and ev.buttons[0] == 1:
                b.move(0, 10, 0)
            if ev.rel[0] < 0 and ev.buttons[0] == 1:
                b.move(0, -10, 0)
            if ev.rel[1] > 0 and ev.buttons[0] == 1:
                b.move(0, 0, 10)
            if ev.rel[1] < 0 and ev.buttons[0] == 1:
                b.move(0, 0, -10)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 4:
                b.move(2, 0, 0)
            if ev.button == 5:
                b.move(-2, 0, 0)
 
    pygame.display.update()