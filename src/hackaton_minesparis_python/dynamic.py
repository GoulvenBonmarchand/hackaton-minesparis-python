from scipy.integrate import odeint
import numpy as np

class Dynamic():
    def __init__(self,goos,k = 100, l0 = 40, m = 100,g =9.81/20,lam = 1.5):
        self._goos = goos
        self.k = k 
        self.l0 = l0
        self.m = m
        self.g = g
        self.lam = lam
    
    @property
    def goos(self):
        return self._goos

    @goos.setter
    def goos(self, new_goos):
        self._goos = new_goos

    def GoosToX(self):
        N = self._goos.shape[0]
        X = np.zeros(4*N)
        for goo in self._goos :
            X[4*goo.id],X[4*goo.id+1], X[4*goo.id+2], X[4*goo.id+3]  = goo.pos[0],goo.vit[0],goo.pos[1],goo.vit[1]
        return X
    
    def update_function(self, X,t):
        N = X.shape[0]
        X_point = np.zeros(N)
        for goo in self._goos :
            X_point[4*goo.id],X_point[4*goo.id+2] = X[4*goo.id+1],X[4*goo.id+3]
            ax = 0.0
            ay = 0.0
            for v in goo.voisins:
                dx = X[4*v.id] - X[4*goo.id]
                dy = X[4*v.id+2] - X[4*goo.id+2]
                dist = np.sqrt(dx*dx + dy*dy)
                if dist < 1e-4:
                    continue
                force = self.k * (dist - self.l0)
                ax += force * (dx / dist)
                ay += force * (dy / dist)
            X_point[4*goo.id+1] = ax - self.lam*X[4*goo.id+1]
            X_point[4*goo.id+3] = ay - self.lam*X[4*goo.id+3] + self.m * self.g
        return X_point

    def next_goos(self):
        # integrate over one frame (~1/24 s) with smaller steps for stability
        t_end = 1/24
        liste_temps = np.linspace(0, t_end, 6)
        return odeint(
            self.update_function,
            self.GoosToX(),
            liste_temps,
            rtol=1e-5,
            atol=1e-7,
            mxstep=2000,
        )[-1]
