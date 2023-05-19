import pygame, random

from Object import *
pygame.init()

GROUND = 500
SIZE = (1000, 800)
FPS = 60
screen = pygame.display.set_mode(SIZE)


box = Object(
    screen=screen,
    pos=(500, 400),
    size=(100, 100),
    vertices=(
        (-1, -1),
        (-1,  1),
        ( 1, -1),
        ( 1,  1)
        )
    )

box.add_force((0, 0), (0, 40))


clock = pygame.time.Clock()
render = True


while render:
    print(box.forces)
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (0, 255, 0), (0, GROUND), (SIZE[0], GROUND))
    box.apply_forces()
    box.move()
    box.draw()
    if box.pos[1] > 600:
        box.velocity = (0, -288)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            render = False

    
    pygame.display.update()
    
exit()