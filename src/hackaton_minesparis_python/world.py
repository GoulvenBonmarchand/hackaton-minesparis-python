import numpy as np
from hackaton_minesparis_python.goo import Goo, StaticGoo
from dynamic import Dynamic

class World:
    def __init__(self):
        self._goos = np.array([])
        self._platforms = np.array([])
        self._dynamic = Dynamic(self._goos)
    
    @property
    def goos(self):
        return self._goos
    
    @property
    def platforms(self):
        return self._platforms
    
    def new_goos(self, new_goos):
        self._goos = np.append(self._goos, new_goos)
    
    def new_platforms(self, new_platforms):
        self._platforms = np.append(self._platforms, new_platforms)

    