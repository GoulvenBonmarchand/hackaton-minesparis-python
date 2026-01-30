import numpy as np
from hackaton_minesparis_python.goo import Goo, StaticGoo
from hackaton_minesparis_python.dynamic import Dynamic

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

    @property
    def dynamic(self):
        return self._dynamic
    
    def new_goos(self, new_goos):
        self._goos = np.append(self._goos, new_goos)
        self._dynamic.goos = self._goos
    
    def new_platforms(self, new_platforms):
        self._platforms = np.append(self._platforms, new_platforms)

    def step(self):
        X_next = self._dynamic.next_goos()
        for goo in self._goos:
            base = 4 * goo.id
            goo.pos = [X_next[base], X_next[base + 2]]
            goo.vit = [X_next[base + 1], X_next[base + 3]]
        return X_next

    
