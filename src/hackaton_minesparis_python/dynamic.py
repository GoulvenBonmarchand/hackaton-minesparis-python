from scipy.integrate import odeint
import numpy as np

class Dynamic():
    def __init__(self,goos,k = 200, l0 = 0.1, m = 0.4,g =9.81/20,lam = 0.15):
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
        ux, uy = np.array([1,0]),np.array([0,1])
        X_point = np.zeros(N)
        for goo in self._goos :
            X_point[4*goo.id],X_point[4*goo.id+2] = X[4*goo.id+1],X[4*goo.id+3]
            X_point[4*goo.id+1] = -self.k*sum([(((X[4*v.id]-X[4*goo.id])**2 + (X[4*v.id+2 ]-X[4*goo.id+ 2])**2)**(1/2) + -self.l0)* np.array([X[4*goo.id]-X[4*v.id],X[4*goo.id+2]-X[4*v.id+2]])@ ux/(((X[4*v.id]-X[4*goo.id])**2 + (X[4*v.id+2 ]-X[4*goo.id+ 2])**2)**(1/2)) for v in goo.voisins]) - self.lam*X[4*goo.voisins+1]
            X_point[4*goo.id+3] = -self.k*sum([(((X[4*v.id]-X[4*goo.id])**2 + (X[4*v.id+2 ]-X[4*goo.id+ 2])**2)**(1/2) + -self.l0)* np.array([X[4*goo.id]-X[4*v.id],X[4*goo.id+2]-X[4*v.id+2]])@ uy/(((X[4*v.id]-X[4*goo.id])**2 + (X[4*v.id+2 ]-X[4*goo.id+ 2])**2)**(1/2)) for v in goo.voisins]) - self.lam*X[4*goo.voisins+3] - self.m * self.g
        return X_point

    def next_goos(self):
        liste_temps = np.linspace(0,24/60,10)
        return odeint(self.update_function, self.GoosToX(), liste_temps)[-1]
