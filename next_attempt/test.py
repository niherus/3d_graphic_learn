import pygame
import math as np
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()

class Camera:
    def __init__(self, fovy, aspect, near, far):
        self.fovy, self.aspect, self.near, self.far = fovy, aspect, near, far
        self.view = 0, 0, 1
        self.frame =  WIDTH / near, HEIGHT / near
        self.light = self.__normalize_vector((0.5, 1, -0.75))
   
    def __check_vertex(self, vertex):
        scalar = sum([self.view[i] * vertex[i] for i in range(3)])
        dist = sum([vertex[i] ** 2 for i in range(3)]) ** 0.5

        return np.acos((scalar / dist)) * 180 / np.pi < self.fovy / 2 and self.near < scalar < self.far
    def __distance(self, vector):
        x, y, z = vector
        return np.sqrt(x * x + y * y + z * z)
    
    def __normalize_vector(self, vector):
        x, y, z, d = *vector, self.__distance(vector)
        return (x / d, y / d, z / d)

         
    def __vertex_projection(self, vertex):
        if self.__check_vertex(vertex):
            k = vertex[2] / self.near
            return vertex[0] / k, vertex[1] / k
        else:
            return None
    def __plane_dist(self, plane, obj):
        vertixes = obj.render()
        d = 0
    
        for i in plane:
            dx, dy, dz = vertixes[i]
            d += self.__distance((dx, dy, dz))
        
        return d // 3
    
    def __plane_normal(self, plane, obj):
        vertixes = obj.render()
        v1, v2, v3 = plane
        x1, y1, z1 = vertixes[v1]
        x2, y2, z2 = vertixes[v2]
        x3, y3, z3 = vertixes[v3]

        return (y1 - y2) * (z1 - z3) - (y1 - y3) * (z1 - z2), (x1 - x3) * (z1 - z2) - (x1 - x2) * (z1 - z3), (x1 - x2) * (y1 - y3) - (x1 - x3) * (y1 - y2) 
        
    def render(self, obj):
        vertices = [self.__vertex_projection(vert) for vert in obj.render()]

        
        for i, j in obj.edges:
            if None not in (vertices[i], vertices[j]):
                x1, y1 = vertices[i]
                x2, y2 =  vertices[j]
                pygame.draw.line(screen, (0, 255, 0), (500 + x1 * self.frame[0], 500 + y1 * self.frame[1]), (500 + x2 * self.frame[0], 500 +  y2 * self.frame[1]))
        
        for vert in vertices:
            if vert is not None:
                x, y = vert
                pygame.draw.circle(screen, (255, 0, 0), (500 + x * self.frame[0], 500 +  y * self.frame[1]), 5)
        plane_on = True
        if plane_on:
            for plane in sorted(obj.planes, key=lambda x: self.__plane_dist(x, obj), reverse=True):
                v1, v2, v3 = plane

                if None not in (vertices[v1], vertices[v2], vertices[v3]):
                    x1, y1 = vertices[v1]
                    x2, y2 = vertices[v2]
                    x3, y3 = vertices[v3]
                    norm = self.__normalize_vector(self.__plane_normal(plane, obj))
                    k = abs(norm[0] * self.light[0] + norm[1] * self.light[1] + norm[2] * self.light[2])

                    pygame.draw.polygon(screen, (int( (1 - k) * 225), int((1 - k) * 225), int((1 - k) * 225)), ((500 + x1 * self.frame[0], 500 + y1  * self.frame[1]), (500 + x2 * self.frame[0], 500 + y2* self.frame[1]), (500 + x3 * self.frame[0], 500 + y3  * self.frame[1])))
            
        
class Obj:       
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
        
        
class Cube(Obj):
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
        self.planes = set()
        for e1 in self.edges:
            for e2 in self.edges:
                if len(set(e1) | set(e2)) == 3:
                    self.planes.add(tuple(set(e1) | set(e2)))
        
        self.planes = list(self.planes)

        self.alpha = 0, 0, 0

class Piramid(Obj):
    def __init__(self, x, y, z, w=10, h=10, d=10):
        self.center = x, y, z
        self.size = w, h, d
        self.vertexes = [
            (-w // 2, h // 2, -d // 2), 
            (-w // 2, h // 2, d // 2), 
            (w // 2, h // 2, -d // 2), 
            (w // 2, h // 2,  d // 2), 
            (0, -h // 2, 0), 
        ]
        self.edges  = [
            (0, 1), 
            (0, 2),
            (0, 4),
            (1, 3),
            (2, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3)
        ]
        self.planes = set()
        for e1 in self.edges:
            for e2 in self.edges:
                if len(set(e1) | set(e2)) == 3:
                    self.planes.add(tuple(set(e1) | set(e2)))
        
        self.planes = list(self.planes)
        self.alpha = 0, 0, 0

class Octahedron(Obj):
    def __init__(self, x, y, z, w=10, h=10, d=10):
        self.center = x, y, z
        self.size = w, h, d
        self.vertexes = [
            (-w // 2, h // 2, -d // 2), 
            (-w // 2, h // 2, d // 2), 
            (w // 2, h // 2, -d // 2), 
            (w // 2, h // 2,  d // 2), 
            (0, -h // 2, 0),
            (0, h, 0), 
        ]
        self.edges  = [
            (0, 1), 
            (0, 2),
            (0, 4),
            (1, 3),
            (2, 3),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3)
        ]
        self.planes = set()
        for e1 in self.edges:
            for e2 in self.edges:
                if len(set(e1) | set(e2)) == 3:
                    self.planes.add(tuple(set(e1) | set(e2)))
        
        self.planes = list(self.planes)
        self.alpha = 0, 0, 0

camera = Camera(170, 1, 5, 200)
pira = Piramid(10, -10, 50)
cube = Cube(0, 10, 50)
octos = Octahedron(-10, -10, 50)
render = True
press = False
while render:
    clock.tick(60)
    pygame.display.set_caption(f"FPS: {clock.get_fps()}")
    screen.fill((0, 0, 0))

    camera.render(pira)
    camera.render(cube)
    camera.render(octos)


    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False
            break
        if ev.type == pygame.KEYDOWN and ev.key == 32:
            press = True
        if ev.type == pygame.KEYUP and ev.key == 32:
            press = False
        if ev.type == pygame.KEYDOWN and ev.key == 100:
            pira.center = (0, -10, 50)
            cube.center = (0, 10, 50)
            pira.alpha = (0, 0, 0)
            cube.alpha = (0, 0, 0)
            
        if ev.type == pygame.MOUSEMOTION:
            if press:
                if ev.rel[0] > 0 and ev.buttons[0] == 1:
                    pira.move(1, 0, 0)
                if ev.rel[0] < 0 and ev.buttons[0] == 1:
                    pira.move(-1, 0, 0)
                if ev.rel[1] > 0 and ev.buttons[0] == 1:
                    pira.move(0, 1, 0)
                if ev.rel[1] < 0 and ev.buttons[0] == 1:
                    pira.move(0, -1, 0)

                if ev.rel[0] > 0 and ev.buttons[2] == 1:
                    pira.rotate(0, -0.1, 0)
                if ev.rel[0] < 0 and ev.buttons[2] == 1:
                    pira.rotate(0, 0.1, 0)
                if ev.rel[1] > 0 and ev.buttons[2] == 1:
                    pira.rotate(0, 0, 0.1)
                if ev.rel[1] < 0 and ev.buttons[2] == 1:
                    pira.rotate(0, 0, -0.1)
            else:
                
                if ev.rel[0] > 0 and ev.buttons[0] == 1:
                    cube.move(1, 0, 0)
                if ev.rel[0] < 0 and ev.buttons[0] == 1:
                    cube.move(-1, 0, 0)
                if ev.rel[1] > 0 and ev.buttons[0] == 1:
                    cube.move(0, 1, 0)
                if ev.rel[1] < 0 and ev.buttons[0] == 1:
                    cube.move(0, -1, 0)

                if ev.rel[0] > 0 and ev.buttons[2] == 1:
                    cube.rotate(0, -0.1, 0)
                if ev.rel[0] < 0 and ev.buttons[2] == 1:
                    cube.rotate(0, 0.1, 0)
                if ev.rel[1] > 0 and ev.buttons[2] == 1:
                    cube.rotate(0, 0, 0.1)
                if ev.rel[1] < 0 and ev.buttons[2] == 1:
                    cube.rotate(0, 0, -0.1)
                
            

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 4:
                cube.move(0, 0, 1)
            if ev.button == 5:
               cube.move(0, 0, -1)

    pygame.display.update()
exit()