import numpy as np

class World:
    def __init__(self):
        self._goos = []
        self._platforms = []
    
    @property
    def goos(self):
        return self._goos
    
    @property
    def platforms(self):
        return self._platforms
    
    @setter
    def goos(self, new_goos):
        self._goos = new_goos   
    
    @setter
    def platforms(self, new_platforms):
        self._platforms = new_platforms

    