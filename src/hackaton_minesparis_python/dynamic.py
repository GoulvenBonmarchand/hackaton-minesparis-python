from scipy.integrate import odeint
import numpy as np

class Dynamic():
    def __init__(self,goos):
        self.goos = goos

    def GooToX(self):
        N = self.goos.shape
        X = X = np.zeros(4*N)
        for goo in self.goos :
            X[4*goo.id],X[4*goo.id+1], X[4*goo.id+2], X[4*goo.id+3]  = goo.pos[0],goo.velocity[0],goo.pos[1],goo.velocity[1]
        return X
    
    def update_function(self, X,t):
        N = X.shape
        mat = np.zeros((N,N))
        ux, uy = np.array([1,0]),np.array([0,1])
        for goo in self.goos :
            for v in goo.voisins:
                d = np.linalg.norm(v.pos - goo.pos)
                mat[4*goo.id+2][4*v.id+2] = -k*(d-l0)*((goo.pos-v.pos) @ ux)/d
                mat[4*goo.id+2][4*v.id+2] = -k*(d-l0)*((goo.pos-v.pos) @ uy)/d - m*g 
        mat = mat + np.diag(-lam* (np.arange(N) % 2 == 0))
        return mat.dot(X)

    #X_sol = odeint(update_function, X, liste_t)
