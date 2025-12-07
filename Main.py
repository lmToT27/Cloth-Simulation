import pygame
import numpy as np
from Cloth import cloth_t

SCREEN_RES = (1600, 900)
FPS = 60
FDELTA_T = 1.0 / 60.0

pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()

ROWS, COLS = 50, 50
SPACING = 10
STIFFNESS = 0.5
SCREEN_OFFSET = (SCREEN_RES[0] - (COLS - 1) * SPACING) / 2

my_cloth = cloth_t(ROWS, COLS, SPACING, STIFFNESS, SCREEN_OFFSET)

start_pos = np.array([0, 0])
end_pos = np.array([0, 0])
is_cutting = False
is_running = True
drag_point_idx = None

prev_mouse_pos = np.array([0.0, 0.0])

while is_running:
    clock.tick(FPS)
    fps_now = clock.get_fps()
    pygame.display.set_caption(f"Cloth Simulation by lmToT27 - FPS: {fps_now:.2f}")

    cur_mouse_pos = np.array(pygame.mouse.get_pos(), dtype = np.float64)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                my_cloth = cloth_t(ROWS, COLS, SPACING, STIFFNESS, SCREEN_OFFSET)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_cutting = True
                start_pos = np.array(event.pos)
                end_pos = start_pos.copy()
            elif event.button == 3:
                drag_point_idx = my_cloth.FindNearestPoint(event.pos)
        if event.type == pygame.MOUSEMOTION and is_cutting:
            start_pos = end_pos.copy()
            end_pos = np.array(event.pos)
            my_cloth.Cut(start_pos, end_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_cutting = False
            elif event.button == 3:
                drag_point_idx = None

    if drag_point_idx is not None:
        if my_cloth.pinned[drag_point_idx]:
            my_cloth.pos[my_cloth.pinned] += cur_mouse_pos - prev_mouse_pos
            my_cloth.old_pos[my_cloth.pinned] = my_cloth.pos[my_cloth.pinned]
        else: 
            my_cloth.pos[drag_point_idx] = cur_mouse_pos.copy()
            my_cloth.old_pos[drag_point_idx] = cur_mouse_pos.copy()
    
    my_cloth.UpdatePoints(FDELTA_T)
    my_cloth.SolveConstraints(5)
    prev_mouse_pos = cur_mouse_pos

    screen.fill("#000000")
    
    if len(my_cloth.lines) > 0:
        start_points = my_cloth.pos[my_cloth.lines[:, 0]]
        end_points = my_cloth.pos[my_cloth.lines[:, 1]]

        if is_cutting: pygame.draw.line(screen, (50, 255, 215), start_pos, end_pos, 2)
        
        for pos in my_cloth.pos:
            pygame.draw.circle(screen, (250, 145, 255), (pos[0], pos[1]), 2)
        for i in range(len(start_points)):
            pygame.draw.line(screen, (250, 200, 255), start_points[i], end_points[i], 1)

    pygame.display.update()

pygame.quit()