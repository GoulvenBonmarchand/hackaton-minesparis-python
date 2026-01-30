from scipy.integrate import odeint
import numpy as np

def update_function(goos,t):
    N = goos.shape
    mat = np.zeros(N)
    ux, uy = np.array([1,0]),np.array([0,1])
    X = np.zeros(4*N)
    for goo in goos :
        X[4*goo.id],X[4*goo.id+1], X[4*goo.id+2], X[4*goo.id+3]  = goo.pos[0],goo.velocity[0],goo.pos[1],goo.velocity[1]
        for v in goo.voisins:
            d = dist(v,goo)
            mat[4*goo.id+2][4*v.id+2] = -k*(d-l0)*((goo.pos-v.pos) @ ux)/d
            mat[4*goo.id+2][4*v.id+2] = -k*(d-l0)*((goo.pos-v.pos) @ uy)/d - m*g 
    mat = mat + np.diag(-lam* (np.arange(N) % 2 == 0))
    return mat.dot(X)

#X_sol = odeint(update_function, goos, liste_t)
