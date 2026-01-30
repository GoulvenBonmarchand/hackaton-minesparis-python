"""Objets "Goo" avec position, vitesse et masse, plus variantes statiques."""

import numpy as np 

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
        #self.ppvoisin() in dev
        #self.ppplateforme() in dev
        
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
    def nm(self):
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
