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
    def __init__(self, pos, world, mass=1.0):
        """Initialise un Goo avec position et masse."""
        self._pos = np.array(pos, dtype=float)
        self._vit = np.zeros(2, dtype=float)
        self._mass = mass
        self._nm = counterGoo()
        self._world = world
        self._voisins = []
        self.ppvoisins()
        self.ppplateforme()

    def ppplateforme(self, distance_plateforme_min=10.0):
        """
        On calcule le projeté de notre goo sur la plateforme convexe
        Pour ce faire, comme la plateforme est convexe, on calcule le projeté orthogonal de notre point sur
        la droite dirigée par les deux points de la plateforme les plus proches de notre goo. Si ce projeté
        appartient à la plateforme alors on renvoie la position du projeté. Sinon on renvoie la position du
        sommet de la plateforme le plus proche de notre goo.
    
        plateforme : liste de points définissant les contours de la plateforme
        goo : repéré par sa position

        """
        for plateforme in self._world.platforms:
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
            if p > 0 and p < d : # si le projet?? appartient ?? la plateforme
                proj =  somme_vecteurs(S1,p*vect(S1,S2)/norme(vect(S1,S2)))
            else:
                proj = S2
            if distance(proj,pos_goo) < distance_plateforme_min: # si le goo est à une distance inférieure à distance_min de la plateforme, il s'accroche à celle-ci. Sinon pas d'interaction
                sgoo = StaticGoo(proj, self._mass)
                self._world.new_goos(sgoo)
                self._voisins.append(sgoo)
            else: 
                pass
    
    def ppvoisins(self, distance_goo_min = 20.0):
        for elt in self._world.goos:
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
    def __init__(self, pos, mass=1.0):
        """Initialise un Goo statique avec position et masse."""
        super().__init__(pos,mass)
    
    @Goo.vit.setter
    def vit(self, new_vit):
        """Ignore toute tentative de modification de vitesse."""
        pass

    @Goo.pos.setter
    def pos(self, new_pos):
        """Ignore toute tentative de modification de position."""
        pass
