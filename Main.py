import pygame
from Cloth import cloth_t

SCREEN_RES = (600, 600)
FPS = 60
FDELTA_T = 1.0 / 60.0

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
time_pool = 0

is_running = True

my_cloth = cloth_t(20, 20, 20, 0.2, 100)

while is_running:
    delta = clock.tick(FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            continue
    
    my_cloth.UpdatePoints(FDELTA_T)
    my_cloth.SolveConstraints(5)

    screen.fill("#000000")
    for u, v in my_cloth.lines:
        pu = my_cloth.points[u].pos
        pv = my_cloth.points[v].pos
        pygame.draw.line(screen, (255, 255, 255), (pu[0], pu[1]), (pv[0], pv[1]), 1)

    pygame.display.update()

pygame.quit()