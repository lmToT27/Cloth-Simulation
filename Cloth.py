from numpy import *

class cloth_t:
    class point_t():
        def __init__(self, x, y, pinned):
            self.pos = array([x, y])
            self.old_pos = array([x, y])
            self.acc = array([0, 0])
            self.pinned = pinned
    
    def __init__(self, ROWS, COLS, SPACING, K): # K is stiffness
        self.ROWS = ROWS
        self.COLS = COLS
        self.SPACING = SPACING
        self.K = K

        self.points = []
        self.lines = []

        for i in range(ROWS):
            for j in range(COLS):
                u = i * COLS + j
                self.points.append(self.point_t(j * SPACING, i * SPACING, i == 0))
                if i > 0:
                    v = u - COLS
                    self.lines.append((u, v))
                if j > 0:
                    v = u - 1
                    self.lines.append((u, v))
    
    def UpdatePoints(self, dt):
        for p in self.points:
            if p.pinned: continue
            tmp = p.pos.copy()
            p.pos = 2 * p.pos - p.old_pos + p.acc * dt * dt
            p.old_pos = tmp
            p.acc = array([0, 0])
    
    def SolveConstraints(self, times):
        for ___ in range(times):
            for u, v in self.lines:
                p1 = self.point[u]
                p2 = self.point[v]
                if p1.pinned and p2.pinned: continue
                L = p2.pos - p1.pos
                Leng = (L[0] * L[0] + L[1] * L[1]) ** 0.5
                if Leng != 0:
                    F = self.K * (Leng - self.SPACING) * (L / Leng)
                    if p1.pinned or p2.pinned:
                        p1.pos += 2 * F * (not p1.pinned) 
                        p2.pos -= 2 * F * (not p2.pinned)
                    else:
                        p1.pos += F
                        p2.pos -= F
                    
                    