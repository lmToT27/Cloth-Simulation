import pygame
import numpy as np
import time
from Cloth import cloth_t
from config import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

my_cloth = cloth_t()

start_pos = np.array([0, 0])
end_pos = np.array([0, 0])
is_cutting = False
is_running = True
drag_point_idx = None

trail = []
prev_mouse_pos = None

while is_running:
    cur_time = time.time()
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
                my_cloth = cloth_t()
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
                if drag_point_idx is not None and drag_point_idx >= COLS:
                    my_cloth.pinned[drag_point_idx] = False
                drag_point_idx = None

    if drag_point_idx is not None:
        if drag_point_idx < COLS:
            l = drag_point_idx - 1
            r = drag_point_idx
            while l >= 0:
                if not my_cloth.connected[l]: break
                l -= 1
            l += 1
            while r + 1 < COLS:
                if not my_cloth.connected[r]: break
                r += 1
            r += 1
            my_cloth.pos[l : r] += cur_mouse_pos - prev_mouse_pos
            my_cloth.old_pos[l : r] = my_cloth.pos[l : r]
        else:
            my_cloth.pinned[drag_point_idx] = True
            my_cloth.pos[drag_point_idx] = cur_mouse_pos.copy()
            my_cloth.old_pos[drag_point_idx] = cur_mouse_pos.copy()
    
    my_cloth.UpdatePoints()
    my_cloth.SolveConstraints()

    screen.fill("#000000")

    if is_cutting:
        cur_mouse_pos = pygame.mouse.get_pos()
        if prev_mouse_pos is not None:
            trail.append((prev_mouse_pos, cur_mouse_pos, cur_time))
        prev_mouse_pos = cur_mouse_pos
    new_trail = []

    for p1, p2, t in trail:
        age = cur_time - t
        if age <= TRAIL_DURATION:
            pygame.draw.line(screen, "#89FFFD", p1, p2, 1)
            new_trail.append((p1, p2, t))
    trail = new_trail

    if len(my_cloth.lines) > 0:
        start_points = my_cloth.pos[my_cloth.lines[:, 0]]
        end_points = my_cloth.pos[my_cloth.lines[:, 1]]
        
        for i in range(len(start_points)):
            pygame.draw.line(screen, "#FFA5F0", start_points[i], end_points[i], 1)
    prev_mouse_pos = cur_mouse_pos

    pygame.display.update()

pygame.quit()