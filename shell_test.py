import pygame
from random import randint as rnd
from math import sin, cos, pi, atan2, hypot
import time
pygame.init()
SIZE = (2000, 1600)
FPS = 60
screen = pygame.display.set_mode(SIZE)

def get_shell(vertices):
    shell_set = set()
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            up = 0
            down = 0
            on = 0
            dx, dy = vertices[i][0] - vertices[j][0], vertices[i][1] - vertices[j][1]
            A = dy
            B = -dx
            C = dx * vertices[i][1] - dy * vertices[i][0] 
            for v in vertices:
                if v != vertices[i] and v != vertices[j]:
                    if A * v[0] + B * v[1] + C > 0:
                        up += 1
                    elif A * v[0] + B * v[1] + C < 0:
                        down += 1
                    else:
                        on += 1
            if (not up or not down) and not on:
                shell_set.add(vertices[i])
                shell_set.add(vertices[j])
                
    x, y = 0, 0
    for dx, dy in shell_set:
        x += dx
        y += dy
    x /= len(shell_set)
    y /= len(shell_set)
    return sorted(shell_set, key=lambda v: atan2(v[0] - x, v[1] - y))

def right_check(trio):
    first = trio[1][0] - trio[0][0], trio[1][1] - trio[0][1]
    second = trio[2][0] - trio[1][0], trio[2][1] - trio[1][1]
    return first[0] * second[1] - first[1] * second[0] > 0
    
    
def get_shell_fast(vertices):
    x_sorted_vertices = sorted(vertices)
    shell_up = [*x_sorted_vertices[:3]]
    for i in range(3, len(vertices)):
        while len(shell_up) > 2 and  not right_check(shell_up[-3:]):
            shell_up.pop(-2)
        shell_up.append(x_sorted_vertices[i])
    while len(shell_up) > 2 and  not right_check(shell_up[-3:]):
        shell_up.pop(-2)
    shell_down = [*x_sorted_vertices[:-4:-1]]
    for i in range(-4, -len(vertices) - 1, -1):
        while len(shell_down) > 2 and not right_check(shell_down[-3:]):
            shell_down.pop(-2)
        shell_down.append(x_sorted_vertices[i])
    while len(shell_down) > 2 and not right_check(shell_down[-3:]):
        shell_down.pop(-2)
    shell_down.pop(0)
    shell_down.pop()
    shell_up.extend(shell_down)
    return shell_up

X = 1000000
poly = [(rnd(0, 2000), rnd(0, 1600))  for i in range(X)]

clock = pygame.time.Clock()
render = True
st = time.perf_counter()
shell2 = get_shell_fast(poly)
print(time.perf_counter() - st)
#st = time.perf_counter()
#shell = get_shell(poly)
#print(time.perf_counter() - st)


while render:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for v in poly:
        pygame.draw.circle(screen, (255, 0, 0), v, 2)
    #pygame.draw.lines(screen, (0, 255, 0), True, shell, 2)
    pygame.draw.lines(screen, (0, 0, 255), True, shell2, 2)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False

    
    pygame.display.update()
    
exit()
    
