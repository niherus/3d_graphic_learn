import pygame
from math import sin, cos, pi, atan2, hypot

class Object:
    def __init__(self, screen, pos, size, vertices):
        self.screen = screen
        self.angle = 0
        self.pos = pos
        self.size = size
        self.__vertices = sorted(vertices, key=lambda v: atan2(v[1], v[0]))
        self.volume = self.volume(self.__vertices) * size[0] * size[1]
        self.density = 0.01
        self.mass = self.volume * self.density
        self.forces = dict()
        self.velocity = (0, 0)
      
    
    def apply_forces(self):
        for place, force in self.forces.items():
            if place[0] or place[1]:
                d = hypot(place[0], place[1])
                f = hypot(force[0], force[1])
                k = (place[0] * force[0] + place[1] * force[1]) / (d)
                self.velocity = (self.velocity[0] + k * place[0], self.velocity[1] + k * place[1])
                self.angle += (pi + atan2(force[1] - self.velocity[1], force[0] - self.velocity[0])) / self.mass
            else:
                self.velocity = (self.velocity[0] + force[0], self.velocity[1] + force[1])
                
    def add_force(self, place, force):
        self.forces[place] = force

    
    def volume(self, vertices):
        s1 = 0
        s2 = 0 
        for i in range(len(vertices)):
            s1 += vertices[i][0] * vertices[i - 1][1]
            s2 += vertices[i - 1][0] * vertices[i][1]
        return abs(s1 - s2) / 2
    
    def __scale(self, vertices):
        return [(x * self.size[0], y * self.size[1]) for x, y in vertices]
        
    def __rotate(self, vertices):
        alp = self.angle
        return [(x * cos(alp) - y * sin(alp), x * sin(alp) + y * cos(alp)) for x, y in vertices]
    
    def move(self):
        self.pos = self.pos[0] + self.velocity[0] / self.mass, self.pos[1] + self.velocity[1] / self.mass
         
        
    def draw(self):
        vert = self.__scale(self.__rotate(self.__vertices))
        vert = [(x + self.pos[0], y + self.pos[1]) for x, y in vert]
        pygame.draw.polygon(self.screen, (0, 0, 255), vert)
        pygame.draw.lines(self.screen, (255, 255, 0), True, vert, 5)