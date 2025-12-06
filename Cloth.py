from numpy import *

class cloth_t:
    class point_t():
        def __init__(self, x, y, pinned):
            self.pos = array([x * 1.0, y * 1.0])
            self.old_pos = array([x * 1.0, y * 1.0])
            self.acc = array([0.0, 0.0])
            self.pinned = pinned

        def Accelerate(self, x, y):
            self.acc += array([x * 1.0, y * 1.0])
    
    def __init__(self, ROWS, COLS, SPACING, K, SCREEN_OFFSET): # K is stiffness
        self.ROWS = ROWS
        self.COLS = COLS
        self.SPACING = SPACING
        self.K = K

        self.points = []
        self.lines = []

        for i in range(ROWS):
            for j in range(COLS):
                u = i * COLS + j
                self.points.append(self.point_t(SCREEN_OFFSET + j * SPACING, SCREEN_OFFSET + i * SPACING, i == 0))
                if i > 0:
                    v = u - COLS
                    self.lines.append((u, v))
                if j > 0:
                    v = u - 1
                    self.lines.append((u, v))

    def UpdatePoints(self, dt):
        for p in self.points:
            if p.pinned: continue
            p.Accelerate(0, 400)
            tmp = p.pos.copy()
            p.pos = 2 * p.pos - p.old_pos + p.acc * dt * dt
            p.old_pos = tmp
            p.acc = array([0.0, 0.0])
    
    def SolveConstraints(self, times):
        for ___ in range(times):
            for u, v in self.lines:
                p1 = self.points[u]
                p2 = self.points[v]
                if p1.pinned and p2.pinned: continue
                L = p2.pos - p1.pos
                Leng = (L[0] * L[0] + L[1] * L[1]) ** 0.5
                if Leng != 0:
                    F = self.K * (Leng - self.SPACING) * (L / Leng)
                    if p1.pinned or p2.pinned:
                        if p2.pinned: p1.pos += 2 * F
                        else: p2.pos -= 2 * F
                    else:
                        p1.pos += F
                        p2.pos -= F