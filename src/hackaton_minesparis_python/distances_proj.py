import numpy as np

def projection(self, plateforme, distance_plateforme_min):
    """
    On calcule le projeté de notre goo sur la plateforme convexe
    Pour ce faire, comme la plateforme est convexe, on calcule le projeté orthogonal de notre point sur
    la droite dirigée par les deux points de la plateforme les plus proches de notre goo. Si ce projeté
    appartient à la plateforme alors on renvoie la position du projeté. Sinon on renvoie la position du
    sommet de la plateforme le plus proche de notre goo.
    
    plateforme : liste de points définissant les contours de la plateforme
    goo : repéré par sa position

    """
    L = plateforme.sommets
    pos_goo = self._pos
    assert len(L)>2
    S1 = None
    d1 = np.float('inf')
    S2 = None
    d2 = np.float('inf')
    for sommet in L:
        if distance(pos_goo, sommet) < d1:
            S1 = sommet
            d1 = distance(pos_goo, sommet)
            if d1 < d2 : # on classe S1 et S2 par distance au goo croissante
                S1,S2 = S2,S1
                d1,d2 = d1,d2
    d = distance(S1,S2)
    p = produit_scalaire(vect(S1,S2), vect(S1,pos_goo))
    if p > 0 and p < d : # si le projeté appartient à la plateforme
        proj =  somme_vecteurs(S1,p*vect(S1,S2)/norme(vect(S1,S2)))
    else:
        proj = S2
    if distance(proj,pos_goo) < distance_plateforme_min: # si le goo est à une distance inférieure à distance_min de la plateforme, il s'accroche à celle-ci. Sinon pas d'interaction
        return proj
    else: 
        return None
    
def creation_lien(self, distance_goo_min):
    for elt in self._world.goos:
        if distance(self._pos, elt._pos) < distance_goo_min:
            self._voisins.append(elt)
    



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

