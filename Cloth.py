import numpy as np
from numba import njit

@njit(fastmath = True)
def UpdatePointsKernel(pos, old_pos, acc, pinned, dt, damping = 0.95, gravity = 400.0):
    num_points = len(pos)
    for i in range(num_points):
        if pinned[i]: continue
        vel = (pos[i] - old_pos[i]) * damping
        tmp = pos[i].copy()
        pos[i] = pos[i] + vel + np.array([0.0, gravity]) * dt * dt
        old_pos[i] = tmp

@njit(fastmath = True)
def SolveConstraintsKernel(pos, lines, lengths, stiffness, times, pinned):
    for _ in range(times):
        for i in range(len(lines)):
            idx1, idx2 = lines[i]
            
            if pinned[idx1] and pinned[idx2]: continue

            p1 = pos[idx1]
            p2 = pos[idx2]
            
            L = p2 - p1
            Leng = (L[0] * L[0] + L[1] * L[1]) ** 0.5
            
            if Leng < 1e-6: continue

            F = (Leng - lengths[i]) / Leng * L * stiffness

            if pinned[idx1] or pinned[idx2]:
                if pinned[idx1]: pos[idx2] -= 2 * F
                else: pos[idx1] += 2 * F
            else:
                pos[idx1] += F
                pos[idx2] -= F

@njit(fastmath = True)
def CheckIntersectKernel(pA, pB, pC, pD):
    Ax, Ay = pA
    Bx, By = pB
    Cx, Cy = pC
    Dx, Dy = pD

    denom = (Ax - Bx) * (Cy - Dy) - (Ay - By) * (Cx - Dx)
    if denom == 0: return False
    
    t = ((Ax - Cx) * (Cy - Dy) - (Ay - Cy) * (Cx - Dx)) / denom
    u = ((Ax - Cx) * (Ay - By) - (Ay - Cy) * (Ax - Bx)) / denom
    
    return (0 < t < 1) and (0 < u < 1)

class cloth_t:
    def __init__(self, ROWS, COLS, SPACING, K, SCREEN_OFFSET):
        self.ROWS = ROWS
        self.COLS = COLS
        self.SPACING = SPACING
        self.K = K # Stiffness

        num_points = ROWS * COLS
        self.pos = np.zeros((num_points, 2), dtype = np.float64)
        self.old_pos = np.zeros((num_points, 2), dtype = np.float64)
        self.pinned = np.zeros(num_points, dtype = np.bool_)

        for i in range(ROWS):
            for j in range(COLS):
                idx = i * COLS + j
                x = SCREEN_OFFSET + j * SPACING
                y = 50 + i * SPACING
                
                self.pos[idx] = [x, y]
                self.old_pos[idx] = [x, y]
                
                if i == 0:
                    self.pinned[idx] = True

        links = []
        rest_lengths = []
        
        for i in range(ROWS):
            for j in range(COLS):
                u = i * COLS + j
                if i > 0:
                    v = u - COLS
                    links.append([u, v])
                    rest_lengths.append(SPACING)
                if j > 0:
                    v = u - 1
                    links.append([u, v])
                    rest_lengths.append(SPACING)
        
        self.lines = np.array(links, dtype = np.int32)
        self.lengths = np.array(rest_lengths, dtype = np.float64)

    def UpdatePoints(self, dt):
        UpdatePointsKernel(self.pos, self.old_pos, None, self.pinned, dt)

    def SolveConstraints(self, times):
        SolveConstraintsKernel(self.pos, self.lines, self.lengths, self.K, times, self.pinned)

    def Cut(self, start_pos, end_pos):
        if len(self.lines) == 0: return

        start_arr = np.array(start_pos, dtype = np.float64)
        end_arr = np.array(end_pos, dtype = np.float64)
        
        mask = []
        for i in range(len(self.lines)):
            u, v = self.lines[i]
            p1 = self.pos[u]
            p2 = self.pos[v]
            
            is_intersect = CheckIntersectKernel(start_arr, end_arr, p1, p2)
            mask.append(not is_intersect)
            
        mask = np.array(mask, dtype = np.bool_)
        self.lines = self.lines[mask]
        self.lengths = self.lengths[mask]

    def FindNearestPoint(self, mouse_pos):
        mouse_arr = np.array(mouse_pos, dtype = np.float64)
        diff = self.pos - mouse_arr
        dist_sq = np.sum(diff ** 2, axis = 1)
        
        min_idx = np.argmin(dist_sq)
        
        if dist_sq[min_idx] < 2500:
            return min_idx
        return None