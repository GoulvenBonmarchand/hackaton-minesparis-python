"""Monde contenant des Goos et des plateformes."""

import numpy as np
from hackaton_minesparis_python.goo import Goo, StaticGoo

class World:
    """Conteneur principal des objets du monde."""
    def __init__(self):
        """Initialise le monde avec des collections vides."""
        self._goos = np.array([])
        self._platforms = np.array([])
    
    @property
    def goos(self):
        """Retourne la liste/collection des Goos."""
        return self._goos
    
    @property
    def platforms(self):
        """Retourne la liste/collection des plateformes."""
        return self._platforms
    
    def new_goos(self, new_goos):
        """Ajoute un ou plusieurs Goos au monde."""
        self._goos = np.append(self._goos, new_goos)
    
    def new_platforms(self, new_platforms):
        """Ajoute une ou plusieurs plateformes au monde."""
        self._platforms = np.append(self._platforms, new_platforms)

    
