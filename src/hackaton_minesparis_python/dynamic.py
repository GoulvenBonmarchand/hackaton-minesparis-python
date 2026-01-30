from scipy.integrate import odeint
import numpy as np

class Dynamic():
    def __init__(self,goos):
        self.goos = goos

    def GoosToX(self):
        N = self.goos.shape[0]
        X = np.zeros(4*N)
        for goo in self.goos :
            X[4*goo.id],X[4*goo.id+1], X[4*goo.id+2], X[4*goo.id+3]  = goo.pos[0],goo.vit[0],goo.pos[1],goo.vit[1]
        return X
    
    def update_function(self, X,t):
        N = X.shape[0]
        mat = np.zeros((N,N))
        ux, uy = np.array([1,0]),np.array([0,1])
        for goo in self.goos :
            for v in goo.voisins:
                vx, goox = np.array(X[4*v.id],X[4*v.id + 2]), np.array(X[4*goo.id],X[4*goo.id + 2])
                d = np.linalg.norm(vx - goox)
                mat[4*goo.id+1][4*v.id+1] = -k*(d-l0)*((goox-vx) @ ux)/d
                mat[4*goo.id+3][4*v.id+3] = -k*(d-l0)*((goox-vx) @ uy)/d - m*g 
        mat += np.diag(-lam* (np.arange(N) % 2 == 0))
        return mat.dot(X)

    def next_goods(self):
        liste_temps = np.arrange(0,24/60,10)
        return odeint(update_function,self.goods, liste_temps)[-1]