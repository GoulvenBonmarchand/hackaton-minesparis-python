import numpy as np

def ppplateforme(self, distance_plateforme_min):
    """
    Calcule le projeté orthogonal de self._pos sur une plateforme convexe.
    Renvoie None si le goo est trop loin de la plateforme.
    """
    for plateforme in self._world.platforms:
        L = plateforme.sommets
        pos_goo = self._pos
        assert len(L) > 2

        liste_projetes = []

        for i in range(len(L)):
            S1 = L[i]
            S2 = L[(i + 1) % len(L)]  # segment consécutif (boucle fermée)
            AB = vect(S1, S2)
            AP = vect(S1, pos_goo)
            norme_AB2 = norme(AB)**2
            t = produit_scalaire(AP, AB) / norme_AB2


            if 0 <= t <= 1:
                proj = S1 + t * AB
            else:
                # si hors du segment, prendre le sommet le plus proche
                if distance(pos_goo, S1) < distance(pos_goo, S2):
                    proj = S1
                else:
                    proj = S2

            liste_projetes.append(proj)

        # Trouver le projeté le plus proche
        m = distance(liste_projetes[0], pos_goo)
        i = 0
        for k in range(1, len(liste_projetes)):
            d = distance(liste_projetes[k], pos_goo)
            if d < m:
                m = d
                i = k

        if m < distance_plateforme_min:
            sgoo = StaticGoo(liste_projetes[i], self._mass)
            self._world.new_goos(sgoo)
            self._voisins.append(sgoo)
        else:
            pass

            
def ppvoisins(self, distance_goo_min = 20.0):
    for elt in self._world.goos:
        if distance(self._pos, elt._pos) < distance_goo_min:
            self._voisins.append(elt)
    



def somme_vecteurs(a,b):
    return np.array([a[0]+b[0],a[1]+b[1]])

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

