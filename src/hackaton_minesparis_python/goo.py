"""Objets "Goo" avec position, vitesse et masse, plus variantes statiques."""

import numpy as np 

from hackaton_minesparis_python.math_goo import distance, produit_scalaire, vect, norme, somme_vecteurs

def make_counter():
    """Retourne un compteur incrémental (fonction fermée)."""
    count = -1
    def counter():
        """Incrémente et retourne la valeur du compteur."""
        nonlocal count
        count += 1
        return count
    return counter
counterGoo = make_counter()

class Goo:
    """Goo mobile avec position, vitesse, masse et voisins."""
    def __init__(self, pos, world, mass=400):
        """Initialise un Goo avec position et masse."""
        self._pos = np.array(pos, dtype=float)
        self._vit = np.zeros(2, dtype=float)
        self._mass = mass
        self._nm = counterGoo()
        self._world = world
        self._voisins = []
        self.ppvoisins()
        self.ppplateforme()

    def ppplateforme(self, distance_plateforme_min=60.0):
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
                sgoo = StaticGoo(liste_projetes[i], self._world, self._mass)
                self._world.new_goos(sgoo)
                self._voisins.append(sgoo)
            else:
                pass
    
    def ppvoisins(self, distance_goo_min = 60.0):
        for elt in self._world.goos :
            if distance(self._pos, elt._pos) < distance_goo_min:
                self._voisins.append(elt)

    @property
    def pos(self):
        """Position 2D (np.ndarray de floats)."""
        return self._pos
    
    @property
    def vit(self):
        """Vitesse 2D (np.ndarray de floats)."""
        return self._vit

    @property
    def mass(self):
        """Masse scalaire du Goo."""
        return self._mass

    @property
    def id(self):
        """Identifiant numérique unique du Goo."""
        return self._nm

    @property
    def voisins(self):
        """Liste des voisins du Goo."""
        return self._voisins

    @pos.setter
    def pos(self, new_pos):
        """Met à jour la position 2D."""
        self._pos = np.array(new_pos, dtype=float)

    @vit.setter
    def vit(self, new_vit):
        """Met à jour la vitesse 2D."""
        self._vit = np.array(new_vit, dtype=float)

class StaticGoo(Goo):
    """Goo immobile: position et vitesse non modifiables."""
    def __init__(self, pos, world, mass=1.0):
        """Initialise un Goo statique avec position et masse."""
        super().__init__(pos, world, mass)

    def ppplateforme(self, distance_plateforme_min=10.0):
        return None
    
    @Goo.vit.setter
    def vit(self, new_vit):
        """Ignore toute tentative de modification de vitesse."""
        pass

    @Goo.pos.setter
    def pos(self, new_pos):
        """Ignore toute tentative de modification de position."""
        pass
