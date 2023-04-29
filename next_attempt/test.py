import pygame
import numpy as np
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Camera:
    def __init__(self, fovy, aspect, near, far):
        self.fovy, self.aspect, self.near, self.far = fovy, aspect, near, far
        self.view = 0, 0, 1
        self.frame = WIDTH / (near * np.sin(self.fovy)), HEIGHT / (near * np.sin(self.fovy))
   
    
    def __check_vertex(self, vertex):
        scalar = sum([self.view[i] * vertex[i] for i in range(3)])
        dist = sum([vertex[i] ** 2 for i in range(3)]) ** 0.5
        return np.arccos((scalar / dist)) * 180 / np.pi < self.fovy / 2 and self.near < scalar < self.far
    def __distance(self, vector):
        x, y, z = vector
        return np.sqrt(x * x + y * y + z * z)
    
    def __normalize_vector(self, vector):
        x, y, z, d = vector, self.__distance(vector)
        return (x / d, y / d, z / d)
         
    def __vertex_projection(self, vertex):
        if self.__check_vertex(vertex):
            k = vertex[2] / self.near
   
            return vertex[0] / k, vertex[1] / k
        else:
            return None
    
    def render(self, obj):
        vertices = [self.__vertex_projection(vert) for vert in obj.render()]

        for i, j in obj.edges:
            if None not in (vertices[i], vertices[j]):
                x1, y1 = vertices[i]
                x2, y2 =  vertices[j]
                pygame.draw.line(screen, (0, 255, 0), (500 + self.frame[0] * x1, 500 + self.frame[1] * y1), (500 + self.frame[0] * x2, 500 + self.frame[1] * y2 ))
        for vert in vertices:
            if vert is not None:
                x, y = vert
                pygame.draw.circle(screen, (255, 0, 0), (500 + self.frame[0] * x, 500 + self.frame[1] * y), 5)
        
        
class Cude:
    def __init__(self, x, y, z, w=10, h=10, d=10):
        self.center = x, y, z
        self.size = w, h, d
        self.vertexes = [
            (-w // 2, -h // 2, -d // 2), 
            (-w // 2, -h // 2, d // 2), 
            (-w // 2, h // 2, -d // 2), 
            (-w // 2, h // 2, d // 2), 
            (w // 2, -h // 2, -d // 2), 
            (w // 2, -h // 2,  d // 2), 
            (w // 2, h // 2, -d // 2), 
            (w // 2, h // 2, d // 2), 
            
        ]
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
        self.alpha = 0, 0, 0
        
    def move(self, dx, dy, dz):
        x, y, z = self.center
        self.center = (x + dx, y + dy, z + dz)
    
    def rotate(self, d_ax, d_ay, d_az):
        ax, ay, az = self.alpha
        self.alpha = (ax + d_ax, ay + d_ay, az + d_az)
    
    def __move(self, vertexes):
        vertexes = vertexes.copy()
        for i in range(len(vertexes)):
            x, y, z = vertexes[i]
            vertexes[i] = (x + self.center[0], y + self.center[1], z + self.center[2])
        return vertexes
    
    def __rotate(self, vertexes):
        vertexes = vertexes.copy()
        
        for i in range(len(vertexes)):
            x, y, z = vertexes[i]
            x, y, z = x * np.cos(self.alpha[0]) - y * np.sin(self.alpha[0]), x * np.sin(self.alpha[0]) + y * np.cos(self.alpha[0]), z
            x, y, z = x * np.cos(self.alpha[1]) + z * np.sin(self.alpha[1]), y, -x * np.sin(self.alpha[1]) + z * np.cos(self.alpha[1])
            x, y, z = x, y * np.cos(self.alpha[2]) - z * np.sin(self.alpha[2]), y * np.sin(self.alpha[2]) + z * np.cos(self.alpha[2])
            vertexes[i] = x, y, z
        return vertexes
    
    def render(self):
        return self.__move(self.__rotate(self.vertexes))
        
        
        

    
camera = Camera(120, 1, 5, 200)

cube = Cude(0, 0, 100)    

render = True
while render:
    clock.tick(60)
    screen.fill((0, 0, 0))
    camera.render(cube)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            start = False
            break
        if ev.type == pygame.MOUSEMOTION:
            if ev.rel[0] > 0 and ev.buttons[0] == 1:
                cube.move(1, 0, 0)
            if ev.rel[0] < 0 and ev.buttons[0] == 1:
                cube.move(-1, 0, 0)
            if ev.rel[1] > 0 and ev.buttons[0] == 1:
                cube.move(0, 1, 0)
            if ev.rel[1] < 0 and ev.buttons[0] == 1:
                cube.move(0, -1, 0)

            if ev.rel[0] > 0 and ev.buttons[2] == 1:
                cube.rotate(0.1, 0, 0)
            if ev.rel[0] < 0 and ev.buttons[2] == 1:
                cube.rotate(-0.1, 0, 0)
            if ev.rel[1] > 0 and ev.buttons[2] == 1:
                cube.rotate(0, 0.1, 0)
            if ev.rel[1] < 0 and ev.buttons[2] == 1:
                cube.rotate(0, -0.1, 0)
            
            
            if ev.rel[0] > 0 and ev.buttons[1] == 1:
                cube.rotate(0, 0, 0.1)
            if ev.rel[0] < 0 and ev.buttons[1] == 1:
                cube.rotate(0, 0, -0.1)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 4:
                cube.move(0, 0, 1)
            if ev.button == 5:
               cube.move(0, 0, -1)

    pygame.display.update()