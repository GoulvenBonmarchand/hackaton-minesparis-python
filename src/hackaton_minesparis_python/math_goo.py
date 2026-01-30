import numpy as np

def somme_vecteurs(a,b):
    return np.array(a[0]+b[0],a[1]+b[1])

def vect(point1, point2):
    return np.array([point2[0]-point1[0], point2[1]-point1[1]])

def norme(x):
    return np.sqrt(produit_scalaire(x,x))

def produit_scalaire(a,b):
    """
    Retoure le produit scalaire entre a et b avec a et b des couples de coordonnées
    
    :param a: np.array([x1,y1])
    :param b: np.array([x2,y2])
    """
    return a[0]*b[0]+a[1]*b[1]

def distance(a,b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

